#include <ESP8266WiFi.h>
#include <WebSocketClient.h>

const char* ssid     = "SSID HERE";
const char* password = "PASSWORD HERE";
char path[] = "/ws";
char host[] = "echo.websocket.org";
  
WebSocketClient webSocketClient;

void setup() {
  pinMode(0, OUTPUT); 
}

void loop() {
  digitalWrite(0, LOW);   
  delay(2000);
  digitalWrite(0, HIGH);
  delay(2000);       
}
