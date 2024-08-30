#include <WiFi.h>
#include <WiFiClientSecure.h>
#include "esp_camera.h"
#include "Arduino.h"
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "base64.h"

// Configuración de la cámara
#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

// Configuración de la red WiFi
const char* ssid = "Fibertel WiFi867 2.4GHz";
const char* password = "0142681436";

// Dirección del servidor y endpoint
const char* serverName = "http://192.168.0.221:8000/image/upload";

void setup() {
  Serial.begin(115200);
  
  // Conectar a la red WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Configurar la cámara
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // Reducir la resolución para evitar problemas de memoria
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 10; // Aumentar para reducir la calidad y ahorrar memoria
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  Serial.println("Camera initialized successfully");
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    camera_fb_t * fb = esp_camera_fb_get();
    Serial.println(WiFi.localIP());

    if(!fb) {
      Serial.println("Failed to capture image");
      delay(10000); // Espera antes de intentar de nuevo
      return;
    }

    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    http.setTimeout(20000);

    StaticJsonDocument<12000> json;
    String base64img = base64::encode(fb->buf, fb->len);
    Serial.println(base64img);
    json["image"] = base64img;
    json["id_person"] = 148;

    String jsonString;
    serializeJson(json, jsonString);
    Serial.println(jsonString);

    int httpResponseCode = http.POST(jsonString);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Respuesta del servidor (" + String(httpResponseCode) + "): " + response);
    } else {
      Serial.println("Error en la petición: " + String(httpResponseCode));
    }

    http.end();
    esp_camera_fb_return(fb); // Liberar la memoria del buffer
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(10000); // Espera antes de tomar otra foto
}
