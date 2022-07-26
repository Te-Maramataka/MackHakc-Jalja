using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ButtonShowHide : MonoBehaviour
{
    GameObject button;

    // Start is called before the first frame update
    void Start()
    {
        button = GameObject.Find("BackToMenu");
        button.SetActive(true); 
    }

    public void OnTriggerEnter (Collider Other)
    {
        button.SetActive(true); 
    }

    public void OnTriggerExit (Collider Other)
    {
        button.SetActive(false); 
    }
}
