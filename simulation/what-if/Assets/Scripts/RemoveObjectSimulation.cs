using UnityEngine;
using System.Collections;

public class RemoveObjectSimulation : PhysicsSimulationsBase
{
    enum SimulationState
    {
        INITIAL_UNSTABLE = 1,
        INITIAL_STABLE = 2,
        FINAL_UNSTABLE = 3,
        FINAL_STABLE = 4
    }

    // The folder to contain our screenshots.
    // If the folder exists we will append numbers to create an empty folder.
    public string folder = "ScreenshotFolder";
    public int frameRate = 30;

    //State of the simulation, whether it is being run 
    private SimulationState state = SimulationState.INITIAL_STABLE;
    private string sceneStateJSON = null;


    protected override void Start()
    {
        base.Start();
        // Set the playback framerate (real time will not relate to game time after this).
        Time.captureFramerate = frameRate;

        // Create the folder
        System.IO.Directory.CreateDirectory(folder);
    }

    void Update()
    {
        if (Time.frameCount == 15)
        {
            sceneStateJSON = SimulationSceneState.getState(gameObjectTemplates);
        }

        if(Time.frameCount == 45)
        {
            if(sceneStateJSON != null)
            {
                SimulationSceneState.setState(sceneStateJSON, gameObjectTemplates);
            }
        }

        if (Time.frameCount == 60)
        {
            stop();
        }
        // Append filename to folder name (format is '0005 shot.png"')
        string name = string.Format("{0}/{1:D04}.png", folder, Time.frameCount);

        // Capture the screenshot to the specified file.
        StartCoroutine(captureScreenshot(name));
    }
}