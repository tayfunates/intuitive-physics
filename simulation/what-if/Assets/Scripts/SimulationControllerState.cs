using UnityEngine;

[System.Serializable]
internal class SimulationControllerState
{
    public int simulationID;
    public int simulationState;
    public int imageWidth;
    public int imageHeight;
    public int removedObjectIndex;

    static public SimulationControllerState fromJSON(string stateStr)
    {
            var state = JsonUtility.FromJson<SimulationControllerState>(stateStr);
            return state;
    }
}