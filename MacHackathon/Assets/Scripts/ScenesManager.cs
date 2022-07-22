using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ScenesManager : MonoBehaviour
{
    public void Loader (string SceneVal)
    {
        SceneManager.LoadScene(SceneVal); //gets a scene name as input and switch to scene with same name
    }
}
