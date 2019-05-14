using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
internal class SimulationSceneState
{
    public List<string> objectStates = new List<string>();

    static public string toJSON(List<SimulationObjectState> objStates)
    {
        if (objStates != null)
        {
            SimulationSceneState sceneState = new SimulationSceneState();
            foreach (SimulationObjectState obj in objStates)
            {
                SimulationColor col = new SimulationColor((SimulationColor.TYPE)obj.color);
                SimulationMaterial mat = new SimulationMaterial((SimulationMaterial.TYPE)obj.material);
                sceneState.objectStates.Add(SimulationObjectState.createJSONFromObject(obj.GetGameObject(), mat, col, obj.size, obj.templateIndex));
            }

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
