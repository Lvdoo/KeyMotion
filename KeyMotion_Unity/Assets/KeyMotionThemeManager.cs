using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class KeyMotionThemeManager : MonoBehaviour
{
    [Header("Références")]
    [SerializeField] private Transform pianoRoot;

    [Header("Couleur actuelle")]
    [SerializeField] private Color selectedGlowColor =
        new Color(0f, 0.25f, 1f, 1f);

    [Header("Preview UI")]
    [SerializeField] private Image colorPreview;

    [Header("Textes des couleurs")]
    [SerializeField] private TMP_Text pinkText;
    [SerializeField] private TMP_Text redText;
    [SerializeField] private TMP_Text purpleText;
    [SerializeField] private TMP_Text greenText;
    [SerializeField] private TMP_Text blueText;
    [SerializeField] private TMP_Text whiteText;

    [Header("Style des textes")]
    [SerializeField] private float normalFontSize = 24f;
    [SerializeField] private float selectedFontSize = 32f;
    [SerializeField] private float normalTextAlpha = 0.55f;
    [SerializeField] private float selectedTextAlpha = 1f;

    private Key_Animation[] keys;
    private TMP_Text[] themeTexts;
    private int currentThemeIndex = 4;

    private const int ThemeCount = 6;

    private void Start()
    {
        if (pianoRoot == null)
        {
            Debug.LogError(
                "PianoRoot n'est pas assigné dans KeyMotionThemeManager."
            );

            return;
        }

        keys = pianoRoot.GetComponentsInChildren<Key_Animation>(true);

        themeTexts = new TMP_Text[]
        {
            pinkText,
            redText,
            purpleText,
            greenText,
            blueText,
            whiteText
        };

        ApplyColorToAllKeys();
        UpdatePreview();
        UpdateSelectedText();
    }

    public void ApplyColorToAllKeys()
    {
        if (keys == null || keys.Length == 0)
        {
            Debug.LogWarning(
                "Aucune touche trouvée par le ThemeManager."
            );

            return;
        }

        foreach (Key_Animation key in keys)
        {
            if (key != null)
            {
                key.SetGlowColor(selectedGlowColor);
            }
        }

        Debug.Log(
            $"Thème appliqué : index {currentThemeIndex}, couleur {selectedGlowColor}"
        );
    }

    public void NextTheme()
    {
        int nextThemeIndex =
            (currentThemeIndex + 1) % ThemeCount;

        SetTheme(nextThemeIndex);
    }

    public void SetPinkTheme()
    {
        SetTheme(0);
    }

    public void SetRedTheme()
    {
        SetTheme(1);
    }

    public void SetPurpleTheme()
    {
        SetTheme(2);
    }

    public void SetGreenTheme()
    {
        SetTheme(3);
    }

    public void SetBlueTheme()
    {
        SetTheme(4);
    }

    public void SetWhiteTheme()
    {
        SetTheme(5);
    }

    private void SetTheme(int themeIndex)
    {
        currentThemeIndex = themeIndex;

        switch (currentThemeIndex)
        {
            case 0:
                selectedGlowColor =
                    new Color(1f, 0.25f, 0.82f, 1f);
                break;

            case 1:
                selectedGlowColor =
                    new Color(1f, 0f, 0f, 1f);
                break;

            case 2:
                selectedGlowColor =
                    new Color(0.65f, 0f, 1f, 1f);
                break;

            case 3:
                selectedGlowColor =
                    new Color(0.1f, 1f, 0.25f, 1f);
                break;

            case 4:
                selectedGlowColor =
                    new Color(0f, 0.25f, 1f, 1f);
                break;

            case 5:
                selectedGlowColor =
                    new Color(1f, 1f, 1f, 1f);
                break;

            default:
                Debug.LogWarning(
                    "Index de thème invalide : " + themeIndex
                );

                return;
        }

        ApplyColorToAllKeys();
        UpdatePreview();
        UpdateSelectedText();
    }

    private void UpdatePreview()
    {
        if (colorPreview == null)
        {
            return;
        }

        Color previewColor = selectedGlowColor;
        previewColor.a = 1f;

        colorPreview.color = previewColor;
    }

    private void UpdateSelectedText()
    {
        if (themeTexts == null)
        {
            return;
        }

        for (int i = 0; i < themeTexts.Length; i++)
        {
            TMP_Text themeText = themeTexts[i];

            if (themeText == null)
            {
                continue;
            }

            bool isSelected = i == currentThemeIndex;

            themeText.fontStyle = isSelected
                ? FontStyles.Bold
                : FontStyles.Normal;

            themeText.fontSize = isSelected
                ? selectedFontSize
                : normalFontSize;

            Color textColor = themeText.color;

            textColor.a = isSelected
                ? selectedTextAlpha
                : normalTextAlpha;

            themeText.color = textColor;
        }
    }
}