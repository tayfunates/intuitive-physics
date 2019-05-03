using UnityEngine;
using System.Collections;
using System.IO;

#if UNITY_EDITOR
using UnityEditor;
#else
#endif

public class PhysicsSimulationsBase : MonoBehaviour
{
    private Camera cam;

    protected GameObject[] gameObjectTemplates = null;

    // Use this for initialization
    protected virtual void Start()
    {
        cam = Camera.main;
        gameObjectTemplates = GameObject.FindGameObjectsWithTag("SimulationObject"); //TODO: Use selected random objects
    }

    // Update is called once per frame
    void Update()
    {

    }

    protected bool isSceneStable()
    {
        if(gameObjectTemplates != null)
        {
            double eps = 1e-5;
            foreach (GameObject obj in gameObjectTemplates)
            {
                if(obj.activeSelf)
                {
                    if (Mathf.Abs(obj.GetComponent<Rigidbody>().velocity.x) > eps ||
                         Mathf.Abs(obj.GetComponent<Rigidbody>().velocity.y) > eps ||
                         Mathf.Abs(obj.GetComponent<Rigidbody>().velocity.z) > eps)
                    {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    protected void stop()
    {
#if UNITY_EDITOR
        if (EditorApplication.isPlaying)
        {
            UnityEditor.EditorApplication.isPlaying = false;
        }
#else
        Application.Quit();
#endif

    }

    protected IEnumerator captureScreenshot(string path, int width, int height)
    {
        yield return new WaitForEndOfFrame();

        RenderTexture rt = new RenderTexture(width, height, 24);
        cam.targetTexture = rt;
        Texture2D screenShot = new Texture2D(width, height, TextureFormat.RGB24, false);
        cam.Render();
        RenderTexture.active = rt;
        screenShot.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        cam.targetTexture = null;
        RenderTexture.active = null; // JC: added to avoid errors
        Destroy(rt);
        byte[] bytes = screenShot.EncodeToPNG();
        System.IO.File.WriteAllBytes(path, bytes);
        Debug.Log(string.Format("Took screenshot to: {0}", path));

    }
}
