//BELORECHENSKAYA
// #define VALVE_OPEN_PIN D5
// #define VALVE_CLOSE_PIN D3

#define VALVE_OPEN_PIN D4
#define VALVE_CLOSE_PIN D3

#define ALT_VALVE 1

#define VALVE_WORK_TIME 5
#define VALVE_FILE "/valve.txt"

bool setup_valve() {
  // pinMode(LED_R_PIN, OUTPUT);
  // pinMode(LED_G_PIN, OUTPUT);
  // pinMode(LED_B_PIN, OUTPUT);

  pinMode(VALVE_OPEN_PIN, OUTPUT);
  digitalWrite(VALVE_OPEN_PIN, HIGH);
  pinMode(VALVE_CLOSE_PIN, OUTPUT);
  digitalWrite(VALVE_CLOSE_PIN, HIGH);
}

void initValve() {
  bool state = readValveState();
  set_valve_state(state);
}

bool valveInputHandler(String value) 
{
  if (value == "open") {
    set_valve_state(true);
    writeValveState(1);
  }
  else if (value == "close") 
  {
    set_valve_state(false);
    writeValveState(0);
  }
}

void set_valve_state(bool state) {
  if (state) {
    #ifdef ALT_VALVE
    digitalWrite(VALVE_CLOSE_PIN, LOW);
    #endif

    digitalWrite(VALVE_OPEN_PIN, LOW);

    blinkDelay(VALVE_WORK_TIME);
    #ifdef ALT_VALVE
    digitalWrite(VALVE_CLOSE_PIN, HIGH);
    #endif

    digitalWrite(VALVE_OPEN_PIN, HIGH);
    Homie.setNodeProperty(bathNode, "valve", "open", true);
  }else {
    digitalWrite(VALVE_CLOSE_PIN, LOW);
    blinkDelay(VALVE_WORK_TIME);
    digitalWrite(VALVE_CLOSE_PIN, HIGH);
    Homie.setNodeProperty(bathNode, "valve", "close", true);
  }
}

void blinkDelay(int sec){
  for(int i = 0; i < sec; i++) {
    // digitalWrite(LED_B_PIN, HIGH);
    delay(300);
    // digitalWrite(LED_B_PIN, LOW);
    // digitalWrite(LED_G_PIN, HIGH);
    delay(300);
    // digitalWrite(LED_G_PIN, LOW);
    // digitalWrite(LED_R_PIN, HIGH);
    delay(300);
    // digitalWrite(LED_R_PIN, LOW);
    // digitalWrite(LED_B_PIN, HIGH);
    delay(100);
  }
  // digitalWrite(LED_B_PIN, LOW);
}

// --------------- functions ----------------------------
bool readValveState() {
  File f = SPIFFS.open(VALVE_FILE, "r");
  if (f) {
    int state = f.parseInt();
    f.close();
    return (state == 1);
  }
}

void writeValveState(int state) {
  File f = SPIFFS.open(VALVE_FILE, "w");
  if (!f) {
    Serial.println("Cant open file!");
    return;
  }
  f.print(String(state));
  f.close();
  Serial.println("Saving done.");  
}
