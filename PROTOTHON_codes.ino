#include <ModbusMaster.h>
#include <DHT.h>
#include <math.h>

// ------------------- Pins -------------------
#define RE_DE_PIN 3        // RS485 DE/RE pin
#define LED_PIN 6          // LED for anomaly alert
#define DHT_PIN 2          // DHT22 data pin

// ------------------- Sensor Setup -------------------
#define DHTTYPE DHT22
DHT dht(DHT_PIN, DHTTYPE);

// ------------------- RS485 -------------------
ModbusMaster node; // RS485 Master

// ------------------- Variables -------------------
float tempC = 25.0;    // temperature
float humidity = 50.0; // humidity

// Anomaly detection variables
float tempAvg = 0, humidAvg = 0;
float tempStd = 0, humidStd = 0;
int N = 1;

// ------------------- Function Declarations -------------------
bool isAnomaly(float val, float avg, float sd, float factor = 2.5);
void updateStats(float &avg, float &sd, float newVal);
void sendToRS485(float temp, float hum);

// ------------------- Setup -------------------
void setup() {
  Serial.begin(9600);

  pinMode(RE_DE_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(RE_DE_PIN, LOW);

  node.begin(2, Serial); // Slave ID 2
  dht.begin();

  Serial.println("Setup complete!");
}

// ------------------- Loop -------------------
void loop() {
  // Read DHT22 sensor
  tempC = dht.readTemperature();
  humidity = dht.readHumidity();

  // Check if readings are valid
  if (isnan(tempC) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  Serial.print("Temp: "); Serial.print(tempC);
  Serial.print(" °C | Humidity: "); Serial.print(humidity); Serial.println(" %");

  // Update statistics
  updateStats(tempAvg, tempStd, tempC);
  updateStats(humidAvg, humidStd, humidity);
  N++;

  // Check anomalies (LED lights if temp or humidity anomalous)
  bool anomaly = false;
  if (isAnomaly(tempC, tempAvg, tempStd) || isAnomaly(humidity, humidAvg, humidStd)) anomaly = true;
  digitalWrite(LED_PIN, anomaly ? HIGH : LOW);

  // Send data over RS485
  sendToRS485(tempC, humidity);

  delay(1500);
}

// ------------------- Functions -------------------
bool isAnomaly(float val, float avg, float sd, float factor) {
  if (sd < 0.1) return false;
  return (val > avg + factor * sd || val < avg - factor * sd);
}

void updateStats(float &avg, float &sd, float newVal) {
  avg = ((avg * (N - 1)) + newVal) / N;
  sd = sqrt(((sd * sd * (N - 1)) + pow(newVal - avg, 2)) / N);
}

void sendToRS485(float temp, float hum) {
  uint16_t temp10 = temp * 10; // convert to integer
  uint16_t hum10  = hum * 10;  // convert to integer

  digitalWrite(RE_DE_PIN, HIGH);  // Enable transmit
  node.setTransmitBuffer(0, temp10);
  node.setTransmitBuffer(1, hum10);
  // Use writeSingleRegister or writeMultipleRegisters if slave is Arduino
  digitalWrite(RE_DE_PIN, LOW);   // Disable transmit
}
