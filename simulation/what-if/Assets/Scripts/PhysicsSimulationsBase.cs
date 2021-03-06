﻿using UnityEngine;
using System.Collections;
using System.IO;
using System.Collections.Generic;
using UnityEngine.Rendering;
using System.Linq;

#if UNITY_EDITOR
using UnityEditor;
#else
#endif

public class PhysicsSimulationsBase : MonoBehaviour
{
    private Camera cam;

    protected GameObject[] gameObjectTemplates = null;
    protected GameObject ground = null;
    internal List<SimulationObjectState> createdSimulationObjects = new List<SimulationObjectState>();

    // Use this for initialization
    protected virtual void Start()
    {
        cam = Camera.main;
        gameObjectTemplates = GameObject.FindGameObjectsWithTag("SimulationObject");
        foreach (GameObject obj in gameObjectTemplates)
        {
            obj.SetActive(false);
            //obj.GetComponent<ReflectionProbe>().enabled = false;
            ReflectionProbe probe = obj.GetComponentInChildren<ReflectionProbe>();
            if(probe != null)
            {
                probe.refreshMode = ReflectionProbeRefreshMode.ViaScripting;
                probe.timeSlicingMode = ReflectionProbeTimeSlicingMode.NoTimeSlicing;
            }
        }
        ground = Resources.FindObjectsOfTypeAll<GameObject>().FirstOrDefault(g => g.CompareTag("Ground"));
    }

    // Update is called once per frame
    void Update()
    {

    }

    protected virtual void ActivateGround()
    {
        if(ground)
        {
            ground.SetActive(true);
        }
    }

    protected bool IsObjectStable(GameObject obj)
    {
        double eps = 1e-5;
        if (obj.activeSelf)
        {
            if (Mathf.Abs(obj.GetComponent<Rigidbody>().velocity.x) > eps ||
                 Mathf.Abs(obj.GetComponent<Rigidbody>().velocity.y) > eps ||
                 Mathf.Abs(obj.GetComponent<Rigidbody>().velocity.z) > eps)
            {
                return false;
            }
        }
        return true;
    }

    protected bool IsSceneStable()
    {
        if(gameObjectTemplates != null)
        {
            double eps = 1e-5;
            foreach (SimulationObjectState state in createdSimulationObjects)
            {
                GameObject obj = state.GetGameObject();
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

    protected void renderReflectionProbes(RenderTexture rt)
    {
        foreach (SimulationObjectState state in createdSimulationObjects)
        {
            GameObject obj = state.GetGameObject();
            if (obj.activeSelf)
            {
                ReflectionProbe probe = obj.GetComponentInChildren<ReflectionProbe>();
                if(probe != null)
                {
                    probe.RenderProbe(rt);
                }
            }
        }
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
        renderReflectionProbes(RenderTexture.active);
        screenShot.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        cam.targetTexture = null;
        RenderTexture.active = null; // JC: added to avoid errors
        Destroy(rt);
        byte[] bytes = screenShot.EncodeToPNG();
        System.IO.File.WriteAllBytes(path, bytes);
        Debug.Log(string.Format("Took screenshot to: {0}", path));

    }
}
