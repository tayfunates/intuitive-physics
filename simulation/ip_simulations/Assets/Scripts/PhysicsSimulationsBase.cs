using UnityEngine;
using System.Collections;
using UnityEditor;

public class PhysicsSimulationsBase : MonoBehaviour
{
    // Use this for initialization
    void Start()
    {

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
