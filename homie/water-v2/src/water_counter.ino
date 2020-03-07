#define CounterNum 2
#define COLD 0
#define HOT 1

int CounterPin[CounterNum] = {D2,D7};
long CounterValues[CounterNum] = {};
Bounce CounterBouncer[CounterNum] = {};

void setup_counters() {
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

void loop_counters() {
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

// --------------- handlers ----------------------------
bool cold_waterInputHandler(String value) 
{
  CounterValues[COLD]=value.toInt();
  writeFile(COLD);
  sendCounterValue(COLD);
  printState(COLD);
}

bool hot_waterInputHandler(String value) 
{
  CounterValues[HOT]=value.toInt();
  writeFile(HOT);
  sendCounterValue(HOT);
  printState(HOT);
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
  Serial.println("Saving done.");  
}

void sendCounterValue(int counterId) {
  String counterName = countrName(counterId);
  Homie.setNodeProperty(bathNode, counterName, String(CounterValues[counterId]), true);
}

void printState(int counterId) {
  Serial.print("Counter[");
  Serial.print(counterId);
  Serial.print("]=");
  Serial.println(CounterValues[counterId]);
}

String countrName(int Id) {
  switch(Id) {
    case HOT:
      return "hot";
    case COLD:
      return "cold";
  }
}

