using UnityEngine;

[System.Serializable]
internal class SimulationObjectState
{
    public int active;
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
            state.position = obj.transform.position;
            state.rotation = obj.transform.rotation;
            state.velocity = obj.GetComponent<Rigidbody>().velocity;
            state.inertiaTensor = obj.GetComponent<Rigidbody>().inertiaTensor;
            state.inertiaTensorRotation = obj.GetComponent<Rigidbody>().inertiaTensorRotation;
            state.angularVelocity = obj.GetComponent<Rigidbody>().angularVelocity;
            state.material = (int)mat.type;
            state.color = (int)col.type;
            state.size = size;
            //state.sceneIndex = sceneIndex;
            state.templateIndex = templateIndex;
            state.active = obj.activeSelf ? 1 : 0;

            return JsonUtility.ToJson(state);
        }

        return "";
    }


    static public SimulationObjectState createObjectFromJSON(string stateStr, GameObject[] gameObjectTemplates, bool active)
    {
        if (gameObjectTemplates != null)
        {
            var state = JsonUtility.FromJson<SimulationObjectState>(stateStr);

            GameObject refObject = gameObjectTemplates[state.templateIndex];
            GameObject obj = Object.Instantiate(refObject);

            SimulationMaterial mat = new SimulationMaterial((SimulationMaterial.TYPE)state.material);
            obj.GetComponent<Rigidbody>().SetDensity(mat.GetDensity());

            SimulationColor col = new SimulationColor((SimulationColor.TYPE)state.color);
            Material newMat = Object.Instantiate(refObject.GetComponent<Renderer>().material);
            newMat.SetColor("_BaseColor", col.GetColor(mat.type));
            obj.GetComponent<Renderer>().material = newMat;

            obj.transform.position = state.position;
            obj.transform.rotation = state.rotation;
            //obj.GetComponent<Rigidbody>().velocity = state.velocity;
            //obj.GetComponent<Rigidbody>().inertiaTensor = state.inertiaTensor;
            //obj.GetComponent<Rigidbody>().inertiaTensorRotation = state.inertiaTensorRotation;
            //obj.GetComponent<Rigidbody>().angularVelocity = state.angularVelocity;

            if(active)
            {
                obj.SetActive(true);
            }

            state.SetGameObject(obj);
            return state;
        }
        return null;
    }
}
