const int COLOR_BUTTON = 4;

int lastButtonState = HIGH;
unsigned long lastPressTime = 0;
const unsigned long debounceDelay = 200;

void setup() {
  Serial.begin(115200);
  pinMode(COLOR_BUTTON, INPUT_PULLUP);
}

void loop() {
  int buttonState = digitalRead(COLOR_BUTTON);
  unsigned long now = millis();

  if (buttonState == LOW && lastButtonState == HIGH && now - lastPressTime > debounceDelay) {
    Serial.println("COLOR|NEXT");
    lastPressTime = now;
  }

  lastButtonState = buttonState;
  delay(10);
}