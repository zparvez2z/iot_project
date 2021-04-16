#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
//#include <SoftwareSerial.h>

//SoftwareSerial s(D6, D5);//rx,tx


const char* ssid = "wifi_name";
const char* password = "wifi_pwd";

//Your Domain name with URL path or IP address with path
const char* serverName = "http://server_url/update-sensor";

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
//unsigned long timerDelay = 600000;
// Set timer to 2 seconds (2000)
unsigned long timerDelay = 2000;
int sensor_value;

void setup() {
//  s.begin(115200);
//  Serial.begin(115200);
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

void led_blink(){
  digitalWrite(2, LOW);   // Turn the LED on by making the voltage LOW
  delay(100);            // Wait for a second
  digitalWrite(2, HIGH);  // Turn the LED off by making the voltage HIGH
}

int v_sensor(){
  return random(61,71);
}

void loop() {
  //Send an HTTP POST request every 10 minutes
  if ((millis() - lastTime) > timerDelay){
//if (s.available() > 0){
    //Check WiFi connection status
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      WiFiClient client;
      // Your Domain name with URL path or IP address with path
      http.begin(client, serverName);

      // Specify content-type header
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      // Data to send with HTTP POST
      String httpRequestData = "sensor1=";
      // get sensor value
//      if (s.available() > 0) {
//        sensor_value = s.read();
        sensor_value = v_sensor();
        Serial.println(sensor_value);
//      }
//      else {
//        sensor_value = -1;
//      }
      // Send HTTP POST request
      int httpResponseCode = http.POST(httpRequestData + sensor_value);
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);

      // Free resources
      http.end();
      // blink led
      led_blink();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}
