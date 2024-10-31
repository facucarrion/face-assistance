#include <WiFi.h>
#include <WebServer.h>
#include <Preferences.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "esp_camera.h" // Librería necesaria para la cámara
#include "base64.h" // Para convertir la imagen a base64

#define DEVICE_ID 1

// Configuración de la cámara
#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

Preferences preferences;

WebServer server(80);

const char* base_url = "http://192.168.2.158:8000";
String ssid;
String password;

unsigned long wifiTimeout = 15000;

String captureImageToBase64() {
  camera_fb_t * fb = NULL;
  fb = esp_camera_fb_get();
  esp_camera_fb_return(fb);
  fb = NULL;
  fb = esp_camera_fb_get();

  if (!fb) {
    Serial.println("Error al capturar la imagen");
    return "";
  }

  String imageBase64 = base64::encode(fb->buf, fb->len);
  esp_camera_fb_return(fb);
  return imageBase64;
}

JsonDocument parseJson(String json) {
  JsonDocument doc;
  deserializeJson(doc, json);

  return doc;
}

String fetch(String endpoint, String method, String body = "") {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    String url = base_url + endpoint;

    Serial.println("Conectando a la URL: " + url);

    http.begin(url);
    int httpResponseCode = -1;

    if (method == "POST") {
      http.addHeader("Content-Type", "application/json");
      Serial.println("Enviando POST con el body: " + body);
      httpResponseCode = http.POST(body);
    } else if (method == "GET") {
      Serial.println("Enviando GET request");
      httpResponseCode = http.GET();
    }

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Respuesta(");
      Serial.print(httpResponseCode);
      Serial.print("): ");
      Serial.println(response);

      http.end();

      return response;
    } else {
      Serial.print("Error en la solicitud HTTP, código: ");
      Serial.println(httpResponseCode);
    }

    http.end();
    return "Error en la solicitud HTTP";
  } else {
    Serial.println("Error: No conectado a WiFi");
    return "Error de conexión a WiFi";
  }
}

String uploadImage(String id_person) {
  String imageBase64 = captureImageToBase64();

  if (imageBase64 == "") {
    Serial.println("Error al obtener la imagen en base64");
    return "Error";
  }

  String jsonBody = "{\"id_person\": " + id_person + ", \"image\": \"" + imageBase64 + "\"}";
  
  String response = fetch("/image/upload", "POST", jsonBody);
  
  Serial.println("Respuesta del servidor: " + response);

  return response;
}

String getIP() {
  if (WiFi.status() == WL_CONNECTED) {
    return "<h2>IP Actual: " + WiFi.localIP().toString() + "</h2>";
  }

  return "";
}

String getConfigId() {
  return String(DEVICE_ID);
}

String getState() {
  String state = fetch("/devices/" + getConfigId() + "/state", "GET");
  return state;
}

String getTempImagePerson() {
  String temp_image = fetch("/temp_images/person/" + getConfigId(), "GET");
  return temp_image;
}

void handleRoot() {
  String html = "<form action='/save' method='POST'>";
  html += "SSID: <input type='text' name='ssid' placeholder='SSID'><br>";
  html += "Password: <input type='password' name='password' placeholder='Password'><br>";
  html += "<input type='submit' value='Guardar'>";
  html += "</form>";
  html += "<h2>ID del DISPOSITIVO: " + String(DEVICE_ID) + "</h2>";
  html += getIP();
  html += "<form action='/reset' method='POST'>";
  html += "<input type='submit' value='Restablecer WiFi'>";
  html += "</form>";
  
  server.send(200, "text/html", html);
}

void handleSave() {
  ssid = server.arg("ssid");
  password = server.arg("password");

  preferences.putString("ssid", ssid);
  preferences.putString("password", password);

  server.send(200, "text/html", "<h1>Datos guardados. Reiniciando...</h1>");
  delay(1000);
  ESP.restart();
}

void handleReset() {
  preferences.clear();
  server.send(200, "text/html", "<h1>Preferencias restablecidas. Reiniciando...</h1>");
  delay(1000);
  ESP.restart();
}

void connectToWiFi() {
  ssid = preferences.getString("ssid", "");
  password = preferences.getString("password", "");

  if (ssid != "") {
    Serial.printf("Conectando a WiFi: %s\n", ssid.c_str());
    WiFi.begin(ssid.c_str(), password.c_str());

    unsigned long startAttemptTime = millis();

    while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < wifiTimeout) {
      delay(500);
      Serial.print(".");
    }

    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("\nConectado a Wi-Fi con éxito");
      Serial.print("Dirección IP: ");
      Serial.println(WiFi.localIP());
      startWebServer();
    } else {
      Serial.println("\nError: No se pudo conectar a Wi-Fi.");
      createAP();
    }
  } else {
    createAP();
  }
}

void createAP() {
  Serial.println("Creando punto de acceso para configuración...");
  WiFi.softAP("ESP32Cam Grupo10");

  Serial.print("Punto de acceso creado. Dirección IP: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);
  server.on("/save", HTTP_POST, handleSave);
  server.on("/reset", HTTP_POST, handleReset);

  server.begin();
  Serial.println("Servidor web iniciado. Accede a http://192.168.4.1");
}

void startWebServer() {
  server.on("/", handleRoot);
  server.on("/save", HTTP_POST, handleSave);
  server.on("/reset", HTTP_POST, handleReset);

  server.begin();
  Serial.printf("Servidor web iniciado. Accede a http://%s\n", WiFi.localIP().toString().c_str());
}

void setup() {
  Serial.begin(115200);

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

  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 10;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x \n", err);
    return;
  }

  preferences.begin("wifi-config", false);

  connectToWiFi();
}

void loop() {
  server.handleClient();

  if (WiFi.status() == WL_CONNECTED) {
    String state = getState();
    state.replace("\"", "");
    
    Serial.print("Valor de state: '");
    Serial.print(state);
    Serial.println("'");
  
    state.trim();
  
    if (state == "Error") {
      Serial.println("❌ ERROR");
    }
  
    if (state == "uploading") {
      String temp = getTempImagePerson();
      bool success = false;
      Serial.print("Valor de temp_image: ");
      Serial.println(temp);
  
      if (temp != "No image") {
        while (success == false) {
          String result = uploadImage(temp);
          JsonDocument parsedResult = parseJson(result);
  
          if (parsedResult["success"] == true) {
            success = true;
          }
  
          delay(5000);
        }
      }
    } else if (state == "capturing") {
      
    }
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(10000);
}
