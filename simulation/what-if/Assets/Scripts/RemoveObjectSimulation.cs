using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class RemoveObjectSimulation : PhysicsSimulationsBase
{
    enum SimulationState
    {
        CREATE_STABLE_CONFIGURATION_THROW = 1,
        CREATE_STABLE_CONFIGURATION_WAIT = 2,
        REMOVE_OBJECT = 3,
    }

    // The folder to contain our screenshots.
    // If the folder exists we will append numbers to create an empty folder.
    public string folder = "ScreenshotFolder";
    public int frameRate = 30;
    private int imageWidth = 512; //Read from json
    private int imageHeight = 512; //Read from json
    private int noObjects = 0;  //Randomly calculated and set in CREATE_STABLE_CONFIGURATION mode.
    private int minNoObjects = 30;
    private int maxNoObjects = 40;
    private int objectThrownFrameInterval = 60;

    //State of the simulation, whether it is being run 
    private SimulationState simState = SimulationState.CREATE_STABLE_CONFIGURATION_THROW; //Read from json
    private string sceneStateJSON = null;

    private int numberOfDistinctObjectUsed = 4; //Rubber/Metal/Small/Big Cubes
    private Vector3 throwMin = new Vector3(-2.0F, 20.0F, -2.0f);
    private Vector3 throwMax = new Vector3(2.0f, 20.0f, 2.0f);
    private int numberOfDistinctColorsUsed = 8;

    protected override void Start()
    {
        base.Start();
        // Set the playback framerate (real time will not relate to game time after this).
        Time.captureFramerate = frameRate;

        noObjects = Random.Range(minNoObjects, maxNoObjects+1);

        // Create the folder
        System.IO.Directory.CreateDirectory(folder);
    }

    void Update()
    {
        if (simState == SimulationState.CREATE_STABLE_CONFIGURATION_THROW)
        {
            if(Time.frameCount % objectThrownFrameInterval == 0)
            {
                AddRandomSimulationObject();
                noObjects--;
            }

            if(noObjects<=0)
            {
                simState = SimulationState.CREATE_STABLE_CONFIGURATION_WAIT;
            }
        }
        else if(simState == SimulationState.CREATE_STABLE_CONFIGURATION_WAIT)
        {
            if (isSceneStable())
            {
                // Append filename to folder name (format is '0005 shot.png"')
                string name = string.Format("{0}/{1:D04}.png", folder, Time.frameCount);

                // Capture the screenshot to the specified file.
                StartCoroutine(captureScreenshot(name, imageWidth, imageHeight));
                stop();
                return;
            }
        }

        /*
        else if(state == SimulationState.REMOVE_OBJECT)
        {
            if(currentRemovedObjectIndex < gameObjectTemplates.Length)
            {
                gameObjectTemplates[currentRemovedObjectIndex].SetActive(false);
                state = SimulationState.FINAL_UNSTABLE;
            }
            else {
                // Append filename to folder name (format is '0005 shot.png"')
                string name = string.Format("{0}/{1:D04}.png", folder, Time.frameCount);

                // Capture the screenshot to the specified file.
                StartCoroutine(captureScreenshot(name, imageWidth, imageHeight));
                stop();
            }
        }

        else if(state == SimulationState.FINAL_UNSTABLE)
        {
            if (isSceneStable())
            {
                state = SimulationState.FINAL_STABLE;
            }
        }
        else if(state == SimulationState.FINAL_STABLE)
        {
            if (sceneStateJSON != null)
            {
                SimulationSceneState.setState(sceneStateJSON, gameObjectTemplates);
                state = SimulationState.INITIAL_STABLE;
                gameObjectTemplates[currentRemovedObjectIndex].SetActive(true);
            }
            currentRemovedObjectIndex++;
        }
        */
    }

    protected virtual void AddRandomSimulationObject()
    {
        int templateIndex = Random.Range(0, numberOfDistinctObjectUsed);
        GameObject refObject = gameObjectTemplates[templateIndex];
        GameObject obj = Object.Instantiate(refObject);
        obj.SetActive(true);

        float x_pos = Random.Range(throwMin.x, throwMax.x);
        float y_pos = Random.Range(throwMin.y, throwMax.y);
        float z_pos = Random.Range(throwMin.z, throwMax.z);

        obj.GetComponent<Rigidbody>().position = new Vector3(x_pos, y_pos, z_pos);

        int colorIndex = Random.Range(0, numberOfDistinctColorsUsed);
        SimulationColor col = new SimulationColor((SimulationColor.TYPE)colorIndex);
        Material newMat = Instantiate(refObject.GetComponent<Renderer>().material);
        newMat.SetColor("_Color", col.GetColor());
        obj.GetComponent<Renderer>().material = newMat;

        SimulationObjectState objState = new SimulationObjectState();
        objState.SetGameObject(obj);
        objState.color = colorIndex;
        objState.templateIndex = templateIndex;
        objState.material = (templateIndex < 2) ? 0 : 1;

        createdSimulationObjects.Add(objState);
    }
}