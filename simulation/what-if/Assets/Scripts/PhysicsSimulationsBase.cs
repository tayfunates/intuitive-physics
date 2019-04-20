using UnityEngine;
using System.Collections;
using UnityEditor;

public class PhysicsSimulationsBase : MonoBehaviour
{
    private Camera cam;

    protected GameObject[] gameObjectTemplates = null;

    // Use this for initialization
    protected virtual void Start()
    {
        cam = Camera.main;
        gameObjectTemplates = GameObject.FindGameObjectsWithTag("SimulationObject");
    }

    // Update is called once per frame
    void Update()
    {

    }

    protected void stop()
    {
        if (EditorApplication.isPlaying)
        {
            UnityEditor.EditorApplication.isPlaying = false;
        }
    }

    protected IEnumerator captureScreenshot(string path)
    {
        yield return new WaitForEndOfFrame();

        Texture2D screenImage = new Texture2D(Screen.width, Screen.height);
        //Get Image from screen
        screenImage.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        screenImage.Apply();
        //Convert to png
        byte[] imageBytes = screenImage.EncodeToPNG();

        //Save image to file
        System.IO.File.WriteAllBytes(path, imageBytes);

    }
}
