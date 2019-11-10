#include <Arduino.h>
#include "WebSocketClient.h"
#include "ESP8266WiFi.h"

WebSocketClient ws;
WiFiClient client;

char path[] = "/ws";
char host[] = "52.90.5.163";

void setup() {
	Serial.begin(115200);
  delay(500);

  pinMode(0, OUTPUT);
  digitalWrite(0, LOW);

	WiFi.begin("FreedomTemple", "cleanTeam2800!");

	Serial.print("Connecting");
	while (WiFi.status() != WL_CONNECTED) {
		delay(500);
		Serial.print(".");
	}
  Serial.print("Connected to WIFI");
  Serial.println(WiFi.localIP());
  Serial.println();

  // Connect to the websocket server
  if (client.connect("52.90.5.163", 8081)) {
    Serial.println("Connected");
  } else {
    Serial.println("Connection failed.");
    while(1) {
      // Hang on failure
    }
  }

  ws.path = path;
  ws.host = host;
  if (ws.handshake(client)) {
    Serial.println("Handshake successful");
  } else {
    Serial.println("Handshake failed.");
    while(1) {
      // Hang on failure
    }  
  }
}

void loop() {
  String data;
	if (!client.connected()) {
    
    Serial.println("Client disconnected.");
    while (1) { 
      // Hang on disconnect. }
    }

	} else {
    
    ws.getData(data);
    if (data.length() > 0) {
      digitalWrite(0, HIGH);
      delay(1000);
      digitalWrite(0, LOW);
      Serial.print("Received data: ");
      Serial.println(data);
    }

    ws.sendData("hi");
	}
	delay(2000);
}
