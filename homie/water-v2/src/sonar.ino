#define SONAR_ECHO D6
#define SONAR_TRIG D7

int currentDistance = 0;
unsigned long timing; // Переменная для хранения точки отсчета

void setup_sonar() {
  pinMode(SONAR_TRIG, OUTPUT);
  pinMode(SONAR_ECHO, INPUT);
}

void loop_sonar() {
  if (millis() - timing > 1000){
    timing = millis();

    digitalWrite(SONAR_TRIG, LOW);
    delayMicroseconds(2);

    digitalWrite(SONAR_TRIG, HIGH);
    delayMicroseconds(10);

    digitalWrite(SONAR_TRIG, LOW);
    int duration = pulseIn(SONAR_ECHO, HIGH);

    int distanceCm = ((duration / 2) / 29.1) * 10;
    Serial.print("distance in cm:");
    Serial.println(distanceCm);

    if (abs(currentDistance - distanceCm) > 50) {
      currentDistance = distanceCm;
      sendDistance();
    }
  }
}

void sendDistance() {
  Homie.setNodeProperty(bathNode, "distance", String(currentDistance), true);
}