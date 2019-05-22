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


    static public List<SimulationObjectState> fromJSON(string sceneStateStr, GameObject[] gameObjectTemplates, int removedObjectIndex)
    {
        List<SimulationObjectState> ret = new List<SimulationObjectState>();
        SimulationSceneState sceneState = JsonUtility.FromJson<SimulationSceneState>(sceneStateStr);
        if (sceneState != null)
        {
            for (int i=0; i < sceneState.objectStates.Count; i++)
            {
                bool active = i != removedObjectIndex;

                SimulationObjectState objState = SimulationObjectState.createObjectFromJSON(sceneState.objectStates[i], gameObjectTemplates, active);
                if (objState != null)
                {
                    ret.Add(objState);
                }
            }
        }
        return ret;
    }
}
