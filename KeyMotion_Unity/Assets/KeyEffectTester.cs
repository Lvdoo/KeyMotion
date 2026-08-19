using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Controls;

public class KeyEffectTester : MonoBehaviour
{
    [SerializeField] private Key_Animation do1;
    [SerializeField] private Key_Animation re1;
    [SerializeField] private Key_Animation mi1;

    private void Update()
    {
        if (Keyboard.current == null)
            return;

        TestKey(Keyboard.current.aKey, do1);
        TestKey(Keyboard.current.zKey, re1);
        TestKey(Keyboard.current.eKey, mi1);

        // Test rapide de DO1 avec espace
        TestKey(Keyboard.current.spaceKey, do1);
    }

    private void TestKey(KeyControl keyboardKey, Key_Animation pianoKey)
    {
        if (keyboardKey == null || pianoKey == null)
            return;

        if (keyboardKey.wasPressedThisFrame)
        {
            pianoKey.SetPressed(true);
        }

        if (keyboardKey.wasReleasedThisFrame)
        {
            pianoKey.SetPressed(false);
        }
    }
}