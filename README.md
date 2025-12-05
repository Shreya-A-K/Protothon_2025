# Protothon_2025
Below is a **ready-to-copy README.md** for your GitHub repo.
It explains both solutions clearly, looks professional, and is fully hackathon-friendly.

---

# 🏭 **Low-Cost Industrial RS485 Sensor Network with Cloud Dashboard & Future ESP32 Mesh + ML Upgrade**

### Protothon 2025 — Team Project

---

## **Overview**

This project presents a **low-cost, modular, industrial-grade monitoring system** designed for MSMEs and small factories.
We built **two scalable architectures**:

### ✅ **Solution 1 — Arduino + RS485 + Firebase Cloud Dashboard (Working Demo)**

A robust, noise-proof RS485 master–slave system with cloud visualization and live anomaly detection.

### ✅ **Solution 2 — ESP32 Mesh + Offline ML + Local Dashboard (Future Upgrade)**

An advanced, internet-free, AI-enabled IoT solution meant for large-scale deployments.

This dual-architecture approach helps us meet the needs of **both small shops (today)** and **large industries (future-ready)**.

---

# **Features**

### **Solution 1 (Demo Build)**

* RS485 long-distance communication (up to 1.2 km)
* Arduino/ESP32 master–slave architecture
* Cloud-based Firestore database
* Streamlit dashboard with live charts
* Telegram alert notifications
* Cost per node: **₹200–₹300**
* Highly reliable in industrial EMI environments

### **Solution 2 (Future Upgrade)**

* ESP32 mesh networking (ESP-NOW / Wi-Fi mesh)
* On-device ML for anomaly detection
* Local storage (LittleFS / SPIFFS)
* Local browser dashboard (no Firebase needed)
* Zero internet cost
* Works in rural/isolated factories

---

# **System Architecture**

## **Solution 1 — Arduino RS485 + Firebase Dashboard**

```
[Sensors] → [RS485 Slave Nodes] → [RS485 Master] → [ESP32/PC] → Firebase → Dashboard
```

* Master polls each slave
* Data logged to Firebase
* Streamlit pulls data & displays graphs
* Alerts sent via Telegram

---

## **Solution 2 — ESP32 Mesh + Offline ML (Future Version)**

```
[ESP32 Nodes with Sensors] ←→ Mesh Network ←→ [Master Node]
           ↓ Local ML Inference
   [Local Dashboard + Local Database]
```

* No cloud dependency
* Predictive ML models deployed on ESP32
* Perfect for large shop floors

---

# **Hardware Used (Demo Version)**

* ESP32 DevKit V1
* Arduino Nano (optional)
* MAX485 / RS485 Module
* DS18B20 / DHT22 Sensor
* Flyback diode
* MOSFET for surge protection
* 100µF smoothing capacitor
* USB cable + jumper wires

---

# 💻 **Software Requirements**

## **Arduino Side**

Install these libraries in Arduino IDE:

```
OneWire
DallasTemperature
DHT sensor library (if using DHT22)
SoftwareSerial (if Nano is used)
```

## **Python Backend**

Create a `requirements.txt` (already provided):

```
firebase_admin
google-cloud-firestore
streamlit
pandas
plotly
requests
pyserial
```

Install using:

```bash
pip install -r requirements.txt
```

---

# 🌐 **Dashboard Features**

* Real-time temperature & humidity charts
* Anomaly detection (warning + critical)
* Telegram notifications
* Historical telemetry table
* Auto-refresh (cached for 60 sec)

---

# 🔔 **Anomaly Detection Logic**

Threshold-based (for demo):

* `temp_warning`, `moist_warning`
* `temp_critical`, `moist_critical`

Alert conditions:

* Warning → Slight deviation
* Critical → Dangerous condition
* Telegram messages sent automatically

Future (Solution 2):

* On-device ML (Random Forest / XGBoost)
* Predictive failures
* Outlier detection

---

# 📦 **Repository Structure**

```
├── arduino/
│   ├── master.ino
│   ├── slave.ino
│
├── dashboard/
│   ├── app.py
│   ├── requirements.txt
│
├── python-serial-uploader/
│   ├── uploader.py
│
├── README.md
└── assets/
    ├── diagrams
    ├── screenshots
```

---

# 🎥 **Demo (Solution 1)**

* Live sensor data on Firebase
* Streamlit dashboard plotting in real-time
* RS485 Arduino nodes responding to polls
* Telegram alerts triggered instantly

---

# 🧠 **Future Scope (Solution 2)**

* ESP32 mesh for 100+ nodes
* Local ML inference (TinyML)
* Offline dashboard hosted by the ESP32 itself
* Predictive maintenance insights
* MQTT-based extensions
* Plug-and-play sensor modules

---

# 🏆 **Why This Project Is cost effective**

* Very low cost (₹200/node)
* Industrial-grade RS485 reliability
* Expandable to ML + Mesh + Edge AI
* Dual architecture → scalable + future-ready
* Ideal for MSMEs and rural manufacturing units

---

# 📜 **License**

MIT License
