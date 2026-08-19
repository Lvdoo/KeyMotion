using UnityEngine;
using UnityEngine.UI;
using System.Collections;

[RequireComponent(typeof(Image))]
public class Key_Animation : MonoBehaviour
{
    [Header("Identité")]
    [SerializeField] private string noteName;

    [Header("Base")]
    [SerializeField] private Color normalColor = Color.white;

    [Header("Glow haut de touche")]
    [SerializeField] private Image topGlowImage;
    [SerializeField] private Color glowColor = new Color(1f, 0.05f, 0.15f, 0.65f);

    [Header("Animation")]
    [SerializeField] private float pressDistance = 4f;
    [SerializeField] private float animationDuration = 0.06f;

    private Image keyImage;
    private RectTransform keyRectTransform;

    private Vector2 normalPosition;
    private Coroutine currentAnimation;
    private bool isPressed;

    public string NoteName => noteName.Trim().ToUpperInvariant();

    private void Awake()
    {
        keyImage = GetComponent<Image>();
        keyRectTransform = GetComponent<RectTransform>();

        normalPosition = keyRectTransform.anchoredPosition;
        keyImage.color = normalColor;

        if (topGlowImage != null)
        {
            Color hiddenGlow = glowColor;
            hiddenGlow.a = 0f;

            topGlowImage.color = hiddenGlow;
            topGlowImage.raycastTarget = false;
        }
    }

    public void SetPressed(bool pressed)
    {
        if (isPressed == pressed)
            return;

        isPressed = pressed;

        if (currentAnimation != null)
            StopCoroutine(currentAnimation);

        currentAnimation = StartCoroutine(AnimateKey(pressed));
    }

    public void SetGlowColor(Color newColor)
    {
        glowColor = newColor;

        if (!isPressed && topGlowImage != null)
        {
            Color hiddenGlow = glowColor;
            hiddenGlow.a = 0f;
            topGlowImage.color = hiddenGlow;
        }
    }

    private IEnumerator AnimateKey(bool pressed)
    {
        Vector2 startPosition = keyRectTransform.anchoredPosition;

        Vector2 targetPosition = pressed
            ? normalPosition + Vector2.down * pressDistance
            : normalPosition;

        Color startGlowColor = topGlowImage != null
            ? topGlowImage.color
            : Color.clear;

        Color targetGlowColor = glowColor;
        targetGlowColor.a = pressed ? glowColor.a : 0f;

        float elapsedTime = 0f;

        while (elapsedTime < animationDuration)
        {
            elapsedTime += Time.deltaTime;

            float progress = Mathf.Clamp01(elapsedTime / animationDuration);
            float smoothProgress = Mathf.SmoothStep(0f, 1f, progress);

            keyRectTransform.anchoredPosition =
                Vector2.Lerp(startPosition, targetPosition, smoothProgress);

            if (topGlowImage != null)
            {
                topGlowImage.color =
                    Color.Lerp(startGlowColor, targetGlowColor, smoothProgress);
            }

            yield return null;
        }

        keyRectTransform.anchoredPosition = targetPosition;

        if (topGlowImage != null)
            topGlowImage.color = targetGlowColor;

        currentAnimation = null;
    }

    private void OnDisable()
    {
        if (currentAnimation != null)
            StopCoroutine(currentAnimation);

        isPressed = false;

        if (keyRectTransform != null)
            keyRectTransform.anchoredPosition = normalPosition;

        if (keyImage != null)
            keyImage.color = normalColor;

        if (topGlowImage != null)
        {
            Color hiddenGlow = glowColor;
            hiddenGlow.a = 0f;
            topGlowImage.color = hiddenGlow;
        }
    }
}