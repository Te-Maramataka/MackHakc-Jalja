using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;
using UnityEngine.UI;

public class SoundManager : MonoBehaviour
{
    [SerializeField] Image SoundOnImage;
    [SerializeField] Image SoundOffImage;
    [SerializeField] Image SFXOnImage;
    [SerializeField] Image SFXOffImage;
    [SerializeField] AudioSource BGM;
    [SerializeField] AudioSource SFX;
    private bool muted = false;
    private bool sfxMuted = false;

    void Start()
    {
        UpdateMusicButtonImage();
        UpdateSFXButtonImage();
        AudioListener.pause = muted;
    }

    public void OnMusicButtonPress()
    {
        if (muted == false)
        {
            muted = true;
            BGM.Pause();
        }
        else
        {
            muted = false;
            BGM.Play();
        }
        UpdateMusicButtonImage();
    }

    private void UpdateMusicButtonImage()
    {
        if (muted == false)
        {
            SoundOnImage.enabled = true;
            SoundOffImage.enabled = false;
        }
        else
        {
            SoundOnImage.enabled = false;
            SoundOffImage.enabled = true;
        }
    }

    public void OnSFXButtonPress()
    {
        if (sfxMuted == false)
        {
            sfxMuted = true;
            SFX.mute = !SFX.mute;
        }
        else
        {
            sfxMuted = false;
            SFX.mute = !SFX.mute;
        }
        UpdateSFXButtonImage();
    }

    private void UpdateSFXButtonImage()
    {
        if (sfxMuted == false)
        {
            SFXOnImage.enabled = true;
            SFXOffImage.enabled = false;
        }
        else
        {
            SFXOnImage.enabled = false;
            SFXOffImage.enabled = true;
        }
    }
}
