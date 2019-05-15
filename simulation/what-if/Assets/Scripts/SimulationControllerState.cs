using UnityEngine;

[System.Serializable]
internal class SimulationControllerState
{
    public int simulationID = 0;
    public int simulationState = 0;
    public int imageWidth = 512;
    public int imageHeight = 512;
    public int removedObjectIndex = 0;
    public int noObjects = 0;
    public int initialBigObjects = 0;
    public float throwMinX = 0.0f;
    public float throwMaxX = 0.0f;
    public float throwMinY = 0.0f;
    public float throwMaxY = 0.0f;
    public float throwMinZ = 0.0f;
    public float throwMaxZ = 0.0f;

    static public SimulationControllerState fromJSON(string stateStr)
    {
            var state = JsonUtility.FromJson<SimulationControllerState>(stateStr);
            return state;
    }
}