using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
internal class SimulationSceneState
{
    public List<string> objectStates = new List<string>();

    static public string getState(GameObject[] objList)
    {
        if (objList != null)
        {
            SimulationSceneState sceneState = new SimulationSceneState();
            /*foreach (GameObject obj in objList)
            {
                sceneState.objectStates.Add(SimulationObjectState.getState(obj));
            }*/

            return JsonUtility.ToJson(sceneState);

        }

        return "";
    }


    static public void setState(string sceneStateStr, GameObject[] objList)
    {
        /*var sceneState = JsonUtility.FromJson<SimulationSceneState>(sceneStateStr);
        if (sceneState != null && objList != null)
        {
            for (int i=0; i < objList.Length; i++)
            {
                GameObject obj = objList[i];
                if(obj != null) 
                {
                    SimulationObjectState.setState(sceneState.objectStates[i], obj);
                }
            }
        }*/
    }
}
