using UnityEngine;

[System.Serializable]
internal class SimulationObjectState
{
    public Vector3 position;
    public Quaternion rotation;

    static public string getState(GameObject obj)
    {
        if(obj != null)
        {
            SimulationObjectState state = new SimulationObjectState();
            state.position = obj.transform.position;
            state.rotation = obj.transform.rotation;

            return JsonUtility.ToJson(state);
        }

        return "";
    }


    static public void setState(string stateStr, GameObject obj)
    {
        var state = JsonUtility.FromJson<SimulationObjectState>(stateStr);
        if(state != null && obj != null)
        {
            obj.transform.position = state.position;
            obj.transform.rotation = state.rotation;
        }
    }
}
