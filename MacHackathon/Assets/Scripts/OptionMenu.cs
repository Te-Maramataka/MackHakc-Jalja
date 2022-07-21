using UnityEngine;
using UnityEngine.Audio;

public class OptionMenu : MonoBehaviour
{
    public AudioMixer audioMixer;

    public void setVolume(float volumeVal)
    {
        audioMixer.SetFloat("Volume", volumeVal);
        //Debug.Log(volumeVal);
    }

    public void setSFXVolume(float SFXvolumeVal)
    {
        audioMixer.SetFloat("SFXVolume", SFXvolumeVal);
        //Debug.Log(volumeVal);
    }
}
