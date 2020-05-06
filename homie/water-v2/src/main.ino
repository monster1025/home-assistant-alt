#include <Homie.h>
#include <Bounce2.h>
#include "FS.h"


HomieNode bathNode("bath", "node");
bool initDone = false;

bool resetHandler(String value) 
{
  //remove config =)
  SPIFFS.remove("/homie/config.json");
  //Homie.reset();
  return true;
}

void setupHandler() {
  bathNode.subscribe("reset", resetHandler);
  bathNode.subscribe("valve", valveInputHandler);
  bathNode.subscribe("hot", hot_waterInputHandler);
  bathNode.subscribe("cold", cold_waterInputHandler);
  Serial.begin(115200);

  initDone = false;
}

void loopHandler() {
  loop_counters();
//  loop_sonar();
}

void setup() {
  Serial.begin(115200);
  SPIFFS.begin();

  Homie.disableResetTrigger();
  Homie.setFirmware("bath", "1.0.4");
  Homie.registerNode(bathNode);
  Homie.setSetupFunction(setupHandler);
  Homie.setLoopFunction(loopHandler);
  Homie.onEvent(onHomieEvent);
  Homie.setup();
}

void loop() {
  Homie.loop();
  
  if (!initDone && Homie.isReadyToOperate()) {
    Serial.println("Running init event");
    setup_valve();
    setup_counters();
    initValve();
    initDone = true;    
  }
}

void onHomieEvent(HomieEvent event) {
  switch(event) {
    case HOMIE_CONFIGURATION_MODE:
      Serial.println("Configuration mode.");
      break;
    case HOMIE_NORMAL_MODE:
      Serial.println("Normal mode.");
      break;
    case HOMIE_OTA_MODE:
      Serial.println("OTA mode.");
      break;
    case HOMIE_ABOUT_TO_RESET:
      Serial.println("Reset mode.");
      break;
    case HOMIE_WIFI_CONNECTED:
      Serial.println("Wifi connected.");
      break;
    case HOMIE_WIFI_DISCONNECTED:
      Serial.println("Wifi disconnected.");
      break;
    case HOMIE_MQTT_CONNECTED:
      Serial.println("MQTT connected.");
      break;
    case HOMIE_MQTT_DISCONNECTED:
      Serial.println("MQTT disconnected.");
      break;
  }
}