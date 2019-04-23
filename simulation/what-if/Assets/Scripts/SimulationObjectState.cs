using UnityEngine;

[System.Serializable]
internal class SimulationObjectState
{
    public Vector3 position;
    public Quaternion rotation;
    public Vector3 velocity;
    public Vector3 inertiaTensor;
    public Quaternion inertiaTensorRotation;
    public Vector3 angularVelocity;

    static public string getState(GameObject obj)
    {
        if(obj != null)
        {
            SimulationObjectState state = new SimulationObjectState();
            state.position = obj.GetComponent<Rigidbody>().position;
            state.rotation = obj.GetComponent<Rigidbody>().rotation;
            state.velocity = obj.GetComponent<Rigidbody>().velocity;
            state.inertiaTensor = obj.GetComponent<Rigidbody>().inertiaTensor;
            state.inertiaTensorRotation = obj.GetComponent<Rigidbody>().inertiaTensorRotation;
            state.angularVelocity = obj.GetComponent<Rigidbody>().angularVelocity;

            return JsonUtility.ToJson(state);
        }

        return "";
    }


    static public void setState(string stateStr, GameObject obj)
    {
        var state = JsonUtility.FromJson<SimulationObjectState>(stateStr);
        if(state != null && obj != null)
        {
            obj.GetComponent<Rigidbody>().position = state.position;
            obj.GetComponent<Rigidbody>().rotation = state.rotation;
            obj.GetComponent<Rigidbody>().velocity = state.velocity;
            obj.GetComponent<Rigidbody>().inertiaTensor = state.inertiaTensor;
            obj.GetComponent<Rigidbody>().inertiaTensorRotation = state.inertiaTensorRotation;
            obj.GetComponent<Rigidbody>().angularVelocity = state.angularVelocity;
        }
    }
}
