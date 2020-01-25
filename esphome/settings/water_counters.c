#include "esphome.h"
#include <Bounce2.h>
#include "FS.h"

#define COLD 0
#define HOT 1

int CounterPin[CounterNum] = {D2,D7};
long CounterValues[CounterNum] = {};
Bounce CounterBouncer[CounterNum] = {};

class MyCustomSensor : public Component, public Sensor {
 public:
  Sensor *cold_sensor = new Sensor();
  Sensor *hot_sensor = new Sensor();

  void setup() override {
	for (int i=0; i<CounterNum; i++) {
		pinMode(CounterPin[i], INPUT_PULLUP);
		CounterBouncer[i].attach(CounterPin[i]);
		CounterBouncer[i].interval(100);
	}
	for (int i=0; i<CounterNum; i++) {
		readCounterFromFile(i);
		sendCounterValue(i);
	}
  }

  void loop() override {
	for (int i=0; i<CounterNum; i++) {
		boolean changed = CounterBouncer[i].update();
		if ( changed ) {
			int value = CounterBouncer[i].read();
			if ( value == LOW) {
				CounterValues[i] = CounterValues[i] + 10;
				sendCounterValue(i);
				writeFile(i);
				printState(i);
			}
		}
	}
  }

  // --------------- functions ----------------------------
	void readCounterFromFile(int counterId) {
	  String filename = "/" + countrName(counterId) + ".txt";
	  File f = SPIFFS.open(filename, "r");
	  if (f) {
		CounterValues[counterId] = f.parseInt();
		f.close();
		printState(counterId);
	  }
	}

	void writeFile(int counterId) {
	  String filename = "/" + countrName(counterId) + ".txt";
	  File f = SPIFFS.open(filename, "w");
	  if (!f) {
		Serial.println("Cant open file!");
		return;
	  }
	  f.print(String(CounterValues[counterId]));
	  f.close();
	  ESP_LOGD("custom", "Saving done.");  
	}

	void sendCounterValue(int counterId) {
	  if (counterId == COLD) {
	  	cold_sensor->publish_state(CounterValues[counterId]);
	  }else if (counterId == HOT) {
	  	hot_sensor->publish_state(CounterValues[counterId]);
	  }
	}

	void printState(int counterId) {
	  ESP_LOGD("custom", "Counter[%d]=%d", counterId, CounterValues[counterId]);
	}
};