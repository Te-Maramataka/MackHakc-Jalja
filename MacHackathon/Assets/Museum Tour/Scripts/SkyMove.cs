using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SkyMove : MonoBehaviour
{
    public float ScrollX = 0.5f;
    public float ScrollY = 0.5f;
    

    void Update()
    {
        float OffsetX = Time.time * ScrollX;
        float OffsetY = Time.time * ScrollY;
        GetComponent<Renderer>().material.SetTextureOffset("Starry Sky",new Vector2(OffsetX, OffsetY));
    }
}