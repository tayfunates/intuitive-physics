using System;

internal class SimulationMaterial
{
    public enum TYPE
    {
        METAL = 0,
        RUBBER = 1,
    }

    public SimulationMaterial(TYPE t)
    {
        type = t;
    }

    public float GetDensity()
    {
        if(type == TYPE.METAL)
        {
            return 10.0F;
        }
        return 5.0F;
    }

    public TYPE type;
}

