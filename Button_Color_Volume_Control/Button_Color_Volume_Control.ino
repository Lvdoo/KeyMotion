const int COLOR_BUTTON = 4;
const int VOLUME_POT = 1;

// Gestion du bouton
int lastButtonState = HIGH;
unsigned long lastPressTime = 0;
const unsigned long debounceDelay = 200;

// Gestion du potentiomètre
int filteredPotValue = 0;
int lastVolumeSent = -1;

unsigned long lastVolumeSendTime = 0;
const unsigned long volumeSendInterval = 50;

void setup()
{
    Serial.begin(115200);

    pinMode(COLOR_BUTTON, INPUT_PULLUP);
    pinMode(VOLUME_POT, INPUT);

    // Lecture sur 12 bits : environ 0 à 4095
    analogReadResolution(12);

    filteredPotValue = analogRead(VOLUME_POT);
}

void loop()
{
    handleColorButton();
    handleVolumePotentiometer();

    delay(5);
}

void handleColorButton()
{
    int buttonState = digitalRead(COLOR_BUTTON);
    unsigned long now = millis();

    if (
        buttonState == LOW &&
        lastButtonState == HIGH &&
        now - lastPressTime > debounceDelay
    )
    {
        Serial.println("COLOR|NEXT");
        lastPressTime = now;
    }

    lastButtonState = buttonState;
}

void handleVolumePotentiometer()
{
    int rawValue = analogRead(VOLUME_POT);

    // Petit filtre pour éviter que le volume tremble
    filteredPotValue =
        (filteredPotValue * 7 + rawValue) / 8;

    int volumePercent = map(
        filteredPotValue,
        0,
        4095,
        0,
        100
    );

    volumePercent = constrain(volumePercent, 0, 100);

    unsigned long now = millis();

    // Envoi uniquement si le volume change suffisamment
    if (
        now - lastVolumeSendTime >= volumeSendInterval &&
        abs(volumePercent - lastVolumeSent) >= 2
    )
    {
        Serial.print("VOLUME|");
        Serial.println(volumePercent);

        lastVolumeSent = volumePercent;
        lastVolumeSendTime = now;
    }
}