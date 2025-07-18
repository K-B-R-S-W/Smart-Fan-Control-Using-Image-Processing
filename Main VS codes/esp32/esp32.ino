#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "SahiDemon";
const char* password = "Sahi448866";

// Fan control pins
const int fanPin1 = 14;
const int fanPin2 = 12;
const int fanPin3 = 13;

// LED pins for different commands
const int ledFanOff = 16;       // LED for fan off
const int ledFanOn = 17;        // LED for fan on
const int ledFanLevel3 = 27;    // LED for fan level 3
const int ledFanSpeedUp = 32;   // LED for fan speed up
const int ledFanSpeedDown = 33; // LED for fan speed down

int currentFanSpeed = 0;

WebServer server(80);

void setFanSpeed(int level) {
  // Turn off all fans
  digitalWrite(fanPin1, LOW);
  digitalWrite(fanPin2, LOW);
  digitalWrite(fanPin3, LOW);

  // Turn on fans according to the speed level
  if (level >= 1) digitalWrite(fanPin1, HIGH);
  if (level >= 2) digitalWrite(fanPin2, HIGH);
  if (level >= 3) digitalWrite(fanPin3, HIGH);

  currentFanSpeed = level;
  Serial.print("Fan speed set to level: ");
  Serial.println(currentFanSpeed);
}

void updateLEDs(int command) {

  digitalWrite(ledFanOff, LOW);
  digitalWrite(ledFanOn, LOW);
  digitalWrite(ledFanLevel3, LOW);
  digitalWrite(ledFanSpeedUp, LOW);
  digitalWrite(ledFanSpeedDown, LOW);


  switch (command) {
    case 0: 
      digitalWrite(ledFanOff, HIGH);   
      break;
    case 1: 
      digitalWrite(ledFanOn, HIGH);    
      break;
    case 3: 
      digitalWrite(ledFanOn, HIGH);  
      digitalWrite(ledFanLevel3, HIGH); 
      break;
    case 4:
      digitalWrite(ledFanOn, HIGH); 
      digitalWrite(ledFanSpeedUp, HIGH); 
      break;
    case 5:
      digitalWrite(ledFanOn, HIGH);   
      digitalWrite(ledFanSpeedDown, HIGH); 
      break;
  }
}


void handleRoot() {
  server.send(200, "text/plain", "Fan Control Active");
}

void handleFanOff() {
  setFanSpeed(0);
  updateLEDs(0);
  server.send(200, "text/plain", "Fan is Off");
}

void handleFanOn() {
  setFanSpeed(1);
  updateLEDs(1);
  server.send(200, "text/plain", "Fan is On (Level 1)");
}

void handleFanLevel3() {
  setFanSpeed(3);
  updateLEDs(3);
  server.send(200, "text/plain", "Fan is On (Level 3)");
}

void handleFanSpeedUp() {
  if (currentFanSpeed < 3) {
    setFanSpeed(currentFanSpeed + 1);
    updateLEDs(4);
    server.send(200, "text/plain", "Fan Speed Increased");
  } else {
    server.send(200, "text/plain", "Fan is already at maximum speed");
  }
}

void handleFanSpeedDown() {
  if (currentFanSpeed > 0) {
    setFanSpeed(currentFanSpeed - 1);
    updateLEDs(5);
    server.send(200, "text/plain", "Fan Speed Decreased");
  } else {
    server.send(200, "text/plain", "Fan is already off");
  }
}

void setup() {
  Serial.begin(115200);

  // Initialize fan pins
  pinMode(fanPin1, OUTPUT);
  pinMode(fanPin2, OUTPUT);
  pinMode(fanPin3, OUTPUT);

  // Initialize LED pins
  pinMode(ledFanOff, OUTPUT);
  pinMode(ledFanOn, OUTPUT);
  pinMode(ledFanLevel3, OUTPUT);
  pinMode(ledFanSpeedUp, OUTPUT);
  pinMode(ledFanSpeedDown, OUTPUT);

  // Start with fan and LEDs off
  setFanSpeed(0);
  updateLEDs(0);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // HTTP server routes
  server.on("/", handleRoot);
  server.on("/fanoff", handleFanOff);
  server.on("/fanon", handleFanOn);
  server.on("/fanlevel3", handleFanLevel3);
  server.on("/fanspeedup", handleFanSpeedUp);
  server.on("/fanspeeddown", handleFanSpeedDown);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}