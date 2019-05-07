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
    public int material;
    public int color;
    public int size;
    //public int sceneIndex;
    public int templateIndex;

    public GameObject GetGameObject() => gameObject;
    public void SetGameObject(GameObject obj) => gameObject = obj;
    private GameObject gameObject;

    static public string createJSONFromObject(GameObject obj, SimulationMaterial mat, SimulationColor col, int size, int templateIndex)
    {
        if (obj != null)
        {
            SimulationObjectState state = new SimulationObjectState();
            state.position = obj.GetComponent<Rigidbody>().position;
            state.rotation = obj.GetComponent<Rigidbody>().rotation;
            state.velocity = obj.GetComponent<Rigidbody>().velocity;
            state.inertiaTensor = obj.GetComponent<Rigidbody>().inertiaTensor;
            state.inertiaTensorRotation = obj.GetComponent<Rigidbody>().inertiaTensorRotation;
            state.angularVelocity = obj.GetComponent<Rigidbody>().angularVelocity;
            state.material = (int)mat.type;
            state.color = (int)col.type;
            state.size = size;
            //state.sceneIndex = sceneIndex;
            state.templateIndex = templateIndex;

            return JsonUtility.ToJson(state);
        }

        return "";
    }


    static public GameObject createObjectFromJSON(string stateStr, GameObject[] gameObjectTemplates)
    {
        if (gameObjectTemplates != null)
        {
            var state = JsonUtility.FromJson<SimulationObjectState>(stateStr);

            GameObject refObject = gameObjectTemplates[state.templateIndex];
            GameObject obj = Object.Instantiate(refObject);
            obj.SetActive(true);

            SimulationMaterial mat = new SimulationMaterial((SimulationMaterial.TYPE)state.material);
            obj.GetComponent<Rigidbody>().SetDensity(mat.GetDensity());

            SimulationColor col = new SimulationColor((SimulationColor.TYPE)state.color);
            Material newMat = Object.Instantiate(refObject.GetComponent<Renderer>().material);
            newMat.SetColor("_Color", col.GetColor());
            obj.GetComponent<Renderer>().material = newMat;

            if (state != null && obj != null)
            {
                obj.GetComponent<Rigidbody>().position = state.position;
                obj.GetComponent<Rigidbody>().rotation = state.rotation;
                obj.GetComponent<Rigidbody>().velocity = state.velocity;
                obj.GetComponent<Rigidbody>().inertiaTensor = state.inertiaTensor;
                obj.GetComponent<Rigidbody>().inertiaTensorRotation = state.inertiaTensorRotation;
                obj.GetComponent<Rigidbody>().angularVelocity = state.angularVelocity;
            }
            return obj;
        }
        return null;
    }
}
