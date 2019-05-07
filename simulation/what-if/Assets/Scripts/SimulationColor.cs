using System;
using UnityEngine;

public class SimulationColor
{
    public enum TYPE
    {
        BLUE = 0,
        BROWN = 1,
        CYAN = 2,
        GRAY = 3,
        GREEN = 4,
        PURPLE = 5,
        RED = 6,
        YELLOW = 7
    }

    public SimulationColor(TYPE t)
    {
        type = t;
    }

    public TYPE type;

    internal Color GetColor(SimulationMaterial.TYPE mat)
    {
        if(mat == SimulationMaterial.TYPE.METAL)
        {
            switch (type)
            {
                case TYPE.BLUE: return new Color(100.0F / 255.0F, 185.0f / 255.0F, 255.0f / 255.0F);
                case TYPE.BROWN: return new Color(171.0F / 255.0F, 130.0f / 255.0F, 20.0f / 255.0F);
                case TYPE.CYAN: return new Color(68.0F / 255.0F, 195.0f / 255.0F, 193.0f / 255.0F);
                case TYPE.GRAY: return new Color(152.0F / 255.0F, 152.0f / 255.0F, 152.0f / 255.0F);
                case TYPE.GREEN: return new Color(40.0F / 255.0F, 152.0f / 255.0F, 40.0f / 255.0F);
                case TYPE.PURPLE: return new Color(175.0F / 255.0F, 101.0f / 255.0F, 221.0f / 255.0F);
                case TYPE.RED: return new Color(152.0F / 255.0F, 40.0f / 255.0F, 40.0f / 255.0F);
                case TYPE.YELLOW: return new Color(243.0F / 255.0F, 242.0f / 255.0F, 81.0f / 255.0F);
            }
        }
        else if(mat == SimulationMaterial.TYPE.RUBBER)
        {
            switch (type)
            {
                case TYPE.BLUE: return new Color(30.0F / 255.0F, 153.0f / 255.0F, 255.0f / 255.0F);
                case TYPE.BROWN: return new Color(120.0F / 255.0F, 94.0f / 255.0F, 23.0f / 255.0F);
                case TYPE.CYAN: return new Color(55.0F / 255.0F, 185.0f / 255.0F, 182.0f / 255.0F);
                case TYPE.GRAY: return new Color(75.0F / 255.0F, 85.0f / 255.0F, 105.0f / 255.0F);
                case TYPE.GREEN: return new Color(40.0F / 255.0F, 152.0f / 255.0F, 40.0f / 255.0F);
                case TYPE.PURPLE: return new Color(122.0F / 255.0F, 17.0f / 255.0F, 188.0f / 255.0F);
                case TYPE.RED: return new Color(152.0F / 255.0F, 40.0f / 255.0F, 40.0f / 255.0F);
                case TYPE.YELLOW: return new Color(176.0F / 255.0F, 175.0f / 255.0F, 37.0f / 255.0F);
            }
        }

        return Color.black;
    }

}
