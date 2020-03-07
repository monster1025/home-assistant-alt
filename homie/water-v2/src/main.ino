#include <Homie.h>
#include <Bounce2.h>
#include "FS.h"


HomieNode bathNode("bath", "node");

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

  setup_valve();
  setup_counters();
//  setup_sonar();
  initValve();
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
  Homie.setup();
}

void loop() {
  Homie.loop();
}