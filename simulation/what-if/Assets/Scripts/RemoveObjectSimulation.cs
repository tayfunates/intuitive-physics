using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.IO;

public class RemoveObjectSimulation : PhysicsSimulationsBase
{
    enum SimulationState
    {
        CREATE_SCENE = 0,
        CREATE_FINAL_UNSTABLE = 1,
        CREATE_FINAL_STABLE = 2,
        SEGMENTATION_SCREENSHOT = 3
    }

    enum CreateSceneState
    {
        THROW = 0,
        WAIT_WITH_PIPE = 1,
        WAIT_WITHOUT_PIPE = 2,
        STOP = 3
    }

    enum RemoveObjectState
    {
        WAIT = 0,
        STOP = 1
    }


    public string simulationFolder = "";

    public int frameRate = 30;
    private int noObjects = 0;  //Randomly calculated

    //State of the simulation, whether it is being run 
    private CreateSceneState createSceneState = CreateSceneState.THROW;
    private RemoveObjectState removeObjectState = RemoveObjectState.WAIT;

    private int numberOfDistinctObjectUsed = 4; //Rubber/Metal/Small/Big Cubes
    private int numberOfDistinctColorsUsed = 8;

    private int maxSimulationFrames = 0;

    private GameObject[] pipeObjects = null;
    private GameObject prevCreatedObject = null;
    private SimulationObjectState prevObjectState = null;

    private SimulationControllerState controllerState = null;

    protected override void Start()
    {
        base.Start();
        // Set the playback framerate (real time will not relate to game time after this).
        Time.captureFramerate = frameRate;

        string controllerJSON = File.ReadAllText("controller.json");
        controllerState = SimulationControllerState.fromJSON(controllerJSON);


        simulationFolder = "Data/";
        string simulationIDString = controllerState.simulationID.ToString().PadLeft(4, '0');
        simulationFolder = string.Concat(simulationFolder, simulationIDString);

        pipeObjects = GameObject.FindGameObjectsWithTag("Pipe");
        if ((SimulationState)controllerState.simulationState == SimulationState.CREATE_SCENE)
        {
            noObjects = controllerState.noObjects;

            // Create the folder
            System.IO.Directory.CreateDirectory(simulationFolder);
            ActivateGround();
        }
        else if (((SimulationState)controllerState.simulationState == SimulationState.CREATE_FINAL_STABLE)
        || ((SimulationState)controllerState.simulationState == SimulationState.SEGMENTATION_SCREENSHOT)
        || ((SimulationState)controllerState.simulationState == SimulationState.CREATE_FINAL_UNSTABLE))
        {
            bool segmentationScreenShot = (SimulationState)controllerState.simulationState == SimulationState.SEGMENTATION_SCREENSHOT;
            bool createUnstable = (SimulationState)controllerState.simulationState == SimulationState.CREATE_FINAL_UNSTABLE;

            int removedObjectIndex = (segmentationScreenShot) ? -1 : controllerState.removedObjectIndex;
            DeactivatePipes();
            CreateSceneFromJSON(removedObjectIndex, controllerState.inputSceneJSON);
            noObjects = createdSimulationObjects.Count;


            if (segmentationScreenShot)
            {
                DisableVolumeSettings();
                SetUnlitMaterials();
            }
            else if(createUnstable)
            {
                WriteGroundTruthInfo(string.Format("FinalUnStable_{0:D04}", controllerState.removedObjectIndex));
                stop();
            }

            ActivateGround();
        }

        maxSimulationFrames = controllerState.maxFramesToWaitPerObject * noObjects;
    }

    void WriteGroundTruthInfo(string infoName)
    {
        string imageFileName = string.Format("{0}/{1}.png", simulationFolder, infoName);
        string jsonFileName = string.Format("{0}/{1}.json", simulationFolder, infoName);
        WriteSceneToJSON(jsonFileName);


        // Capture the screenshot to the specified file.
        StartCoroutine(captureScreenshot(imageFileName, controllerState.imageWidth, controllerState.imageHeight));
    }

    void Update()
    {
        if((SimulationState)controllerState.simulationState == SimulationState.CREATE_SCENE)
        {
            if (createSceneState == CreateSceneState.THROW)
            {
                if (prevCreatedObject == null)
                {
                    AddRandomSimulationObject();
                }
                else
                {
                    if(IsObjectStable(prevCreatedObject))
                    {
                        if(IsCreatedObjectValid(prevCreatedObject))
                        {
                            createdSimulationObjects.Add(prevObjectState);
                            noObjects--;
                            prevCreatedObject = null;
                            prevObjectState = null;
                        }
                        else
                        {
                            prevCreatedObject.SetActive(false);
                            Destroy(prevCreatedObject);
                            prevCreatedObject = null;
                            prevObjectState = null;
                        }
                    }
                }

                if (noObjects <= 0)
                {
                    createSceneState = CreateSceneState.WAIT_WITH_PIPE;
                }
            }
            else if (createSceneState == CreateSceneState.WAIT_WITH_PIPE)
            {
                if (IsSceneStable())
                {
                    bool changeState = true;
                    foreach (GameObject obj in pipeObjects)
                    {
                        if(obj.activeSelf == true)
                        {
                            changeState = false;
                            obj.SetActive(false);
                            break;
                        }

                    }
                    if (changeState)
                    {
                        createSceneState = CreateSceneState.WAIT_WITHOUT_PIPE;
                    }
                }
            }
            else if(createSceneState == CreateSceneState.WAIT_WITHOUT_PIPE)
            {
                if(IsSceneStable())
                {
                    // Append filename to folder name (format is '0005 shot.png"')
                    WriteGroundTruthInfo("InitialStable");
                    createSceneState = CreateSceneState.STOP;
                }
            }
            else if (createSceneState == CreateSceneState.STOP)
            {
                if(controllerState.stopWaitFrame<=0)
                {
                    stop();
                }
                controllerState.stopWaitFrame--;
            }

            if(maxSimulationFrames != 0 && Time.frameCount >= maxSimulationFrames)
            {
                //Reset simulation by deleting the directory
                System.IO.Directory.Delete(simulationFolder);
                stop();
            }
        }

        else if ((SimulationState)controllerState.simulationState == SimulationState.CREATE_FINAL_STABLE)
        {
            if(removeObjectState == RemoveObjectState.WAIT)
            {
                if (IsSceneStable())
                {
                    WriteGroundTruthInfo(string.Format("FinalStable_{0:D04}", controllerState.removedObjectIndex));
                    removeObjectState = RemoveObjectState.STOP;
                }
            }
            else if (removeObjectState == RemoveObjectState.STOP)
            {
                if (controllerState.stopWaitFrame <= 0)
                {
                    stop();
                }
                controllerState.stopWaitFrame--;
            }

            if (maxSimulationFrames != 0 && Time.frameCount >= maxSimulationFrames)
            {
                //Reset simulation by deleting the directory
                System.IO.Directory.Delete(simulationFolder);
                stop();
            }
        }
        if ((SimulationState)controllerState.simulationState == SimulationState.SEGMENTATION_SCREENSHOT)
        {
            string imageFileName = string.Format("{0}/{1}_VisibleSeg.png", simulationFolder, Path.GetFileNameWithoutExtension(controllerState.inputSceneJSON));
            StartCoroutine(captureScreenshot(imageFileName, controllerState.imageWidth, controllerState.imageHeight));
            stop();
        }
    }

    protected virtual void DisableVolumeSettings()
    {
        var volumeSettings = GameObject.FindGameObjectsWithTag("DisabledInSegmentation");
        foreach (GameObject obj in volumeSettings)
        {
            obj.SetActive(false);
        }
    }

    protected virtual void DeactivatePipes()
    {
        if(pipeObjects != null)
        {
            foreach (GameObject obj in pipeObjects)
            {
                obj.SetActive(false);
            }
        }
    }

    protected virtual void SetUnlitMaterials()
    { 
        float colorInc = 1.0f / noObjects;

        Material unlitMat = new Material(Shader.Find("Unlit/Color"));

        int i = 1;
        foreach (SimulationObjectState state in createdSimulationObjects) {
            GameObject obj = state.GetGameObject();
            Renderer objRend = obj.GetComponent<Renderer>();

            float grayColor = i * colorInc;
            objRend.material = Object.Instantiate(unlitMat);
            objRend.material.SetColor("_Color", new Color(grayColor, grayColor, grayColor));
            i++;
        }

        
        Renderer rend = ground.GetComponent<Renderer>();
        if (rend.materials != null)
        {
            Material newMat = Object.Instantiate(unlitMat);
            newMat.SetColor("_Color", new Color(0.0f, 0.0f, 0.0f));
            var mats = new Material[rend.materials.Length];
            for (var j = 0; j < rend.materials.Length; j++)
            {
                mats[j] = newMat;
            }
            rend.materials = mats;
        }

    }

    protected bool IsCreatedObjectValid(GameObject obj)
    {
        //Contact validness checks the transformed bounding box of the object by looking the lower face
        //Lower face is transformed using object's current transform matrix
        //The space of transformed box is not important, since we will only calculate a normal from a triangle of the face and compare with 6 ground truth directions to consider flipped orientations
        Bounds meshBounds = obj.GetComponent<MeshRenderer>().bounds;
        Vector3[] lowerBoundsWithoutTransform = new[] { new Vector3(meshBounds.center.x - meshBounds.extents.x, meshBounds.center.y - meshBounds.extents.y, meshBounds.center.z - meshBounds.extents.z), 
                                        new Vector3(meshBounds.center.x + meshBounds.extents.x, meshBounds.center.y - meshBounds.extents.y, meshBounds.center.z - meshBounds.extents.z),
                                        new Vector3(meshBounds.center.x + meshBounds.extents.x, meshBounds.center.y - meshBounds.extents.y, meshBounds.center.z + meshBounds.extents.z)};


        List<Vector3> lowerBounds = new List<Vector3>();
        foreach (Vector3 lbpt in lowerBoundsWithoutTransform)
        {
            lowerBounds.Add(obj.transform.worldToLocalMatrix * lbpt);
        }


        const float contactValidnessAngleThres = 20f;

        /*
        Dir = (B - A) x(C - A)
        Norm = Dir / len(Dir) */

        Vector3 Dir = Vector3.Normalize(Vector3.Cross((lowerBounds[1] - lowerBounds[0]), (lowerBounds[2] - lowerBounds[0])));

        bool contactValid = false;

        Vector3[] gtConfigurationsAfterTransform = new[] { new Vector3(-1f, 0f, 0f),
                                                            new Vector3(1f, 0f, 0f),
                                                            new Vector3(0f, -1f, 0f),
                                                            new Vector3(0f, 1f, 0f),
                                                            new Vector3(0f, 0f, -1f),
                                                            new Vector3(0f, 0f, 1f)};

        foreach(Vector3 gtConf in gtConfigurationsAfterTransform)
        {
            float angle = Vector3.Angle(gtConf, Dir);
            if(angle < contactValidnessAngleThres)
            {
                contactValid = true;
                break;
            }
        }

        if (contactValid)
        {
            foreach (GameObject pipeObject in pipeObjects)
            {
                Bounds pipeBounds = pipeObject.GetComponentInChildren<MeshCollider>().bounds;
                if (pipeBounds.Contains(obj.transform.position))
                {
                    return true;
                }
            }
        }

        return false;
    }


    protected virtual void CreateSceneFromJSON(int removedObjectIndex, string json)
    {
        string jsonFileName = string.Format("{0}/{1}", simulationFolder, json);
        string sceneJSON = File.ReadAllText(jsonFileName);
        createdSimulationObjects = SimulationSceneState.fromJSON(sceneJSON, gameObjectTemplates, removedObjectIndex);
    }

    protected virtual void AddRandomSimulationObject()
    {
        int templateIndex = 0;


        if (controllerState.noObjects - noObjects < controllerState.initialBigObjects)
        {
            templateIndex = Random.Range(0, numberOfDistinctObjectUsed / 2);
            templateIndex = templateIndex * 2 + 1;
        }
        else
        {
            templateIndex = Random.Range(0, numberOfDistinctObjectUsed);
        }

        /*
        if (controllerState.noObjects - noObjects < controllerState.initialBigObjects)
        {
            templateIndex = 3;
        }
        else
        {
            templateIndex = Random.Range(2, numberOfDistinctObjectUsed);
        }
        */

        GameObject refObject = gameObjectTemplates[templateIndex];
        GameObject obj = Object.Instantiate(refObject);
        obj.SetActive(true);

        float x_pos = Random.Range(controllerState.throwMinX, controllerState.throwMaxX);
        float y_pos = Random.Range(controllerState.throwMinY, controllerState.throwMaxY);
        float z_pos = Random.Range(controllerState.throwMinZ, controllerState.throwMaxZ);

        obj.GetComponent<Rigidbody>().position = new Vector3(x_pos, y_pos, z_pos);

        SimulationObjectState objState = new SimulationObjectState();
        objState.material = (templateIndex < 2) ? 0 : 1;
        objState.size = (templateIndex % 2 == 0) ? 0 : 1;

        int colorIndex = Random.Range(0, numberOfDistinctColorsUsed);
        SimulationColor col = new SimulationColor((SimulationColor.TYPE)colorIndex);
        Material newMat = Instantiate(refObject.GetComponent<Renderer>().material);
        newMat.SetColor("_BaseColor", col.GetColor((SimulationMaterial.TYPE)objState.material));
        obj.GetComponent<Renderer>().material = newMat;


        objState.SetGameObject(obj);
        objState.color = colorIndex;
        objState.templateIndex = templateIndex;

        prevObjectState = objState;
        prevCreatedObject = obj;
    }

    protected virtual void WriteSceneToJSON(string filePath)
    {
        string sceneJSON = SimulationSceneState.toJSON(createdSimulationObjects);

        StreamWriter sw = File.CreateText(filePath); // if file doesnt exist, make the file in the specified path
        sw.Close();

        File.WriteAllText(filePath, sceneJSON); // fill the file with the data(json)
    }
}