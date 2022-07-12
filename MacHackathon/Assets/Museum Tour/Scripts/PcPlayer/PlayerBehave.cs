using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerBehave : MonoBehaviour
{
    public float moveSpeed = 10f;
    public Transform orientation;
    public Rigidbody rb;

    float LeftRight = 0f;
    float BackForward = 0f;
    Vector3 moveDirection;

    // Start is called before the first frame update
    void Start()
    {
        rb.freezeRotation = true;
    }

    void FixedUpdate()
    {
        LeftRight = Input.GetAxisRaw("Horizontal");
        BackForward = Input.GetAxisRaw("Vertical");
        moveDirection = orientation.forward * BackForward + orientation.right * LeftRight;
        rb.AddForce(moveDirection.normalized * moveSpeed * 10f, ForceMode.Force);
    }
}
