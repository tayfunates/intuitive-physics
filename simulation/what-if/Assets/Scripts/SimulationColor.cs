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

    public Color GetColor()
    {
        switch(type)
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
        return Color.black;
    }

}
