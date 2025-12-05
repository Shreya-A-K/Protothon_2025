import serial
import time
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# ------------------------------------------------------------
# 1. FIREBASE INITIALIZATION (SAFE VERSION)
# ------------------------------------------------------------
# Make sure the file "serviceAccountKey.json" is added to .gitignore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
collection_ref = db.collection("SensorReadings")   # Firestore collection

print("Firebase initialized!")


# ------------------------------------------------------------
# 2. SERIAL SETUP
# ------------------------------------------------------------
COM_PORT = "COM4"      # Change if needed
BAUD_RATE = 9600

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Connected to Arduino on {COM_PORT}\n")
except Exception as e:
    print("Error: Cannot connect to Arduino:", e)
    exit()


# ------------------------------------------------------------
# 3. MAIN LOOP – READ + UPLOAD
# ------------------------------------------------------------
print("Reading and uploading sensor data...\n")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()

        if not line:
            continue

        print("Received:", line)

        # Expecting "Temp: 26.80 °C | Humidity: 58.60 %"
        try:
            temp_part = line.split("|")[0].strip()
            hum_part = line.split("|")[1].strip()

            temperature = float(temp_part.split(":")[1].replace("°C", "").strip())
            humidity = float(hum_part.split(":")[1].replace("%", "").strip())
        except Exception as parse_error:
            print("Parse error:", parse_error)
            continue

        data = {
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": datetime.utcnow().isoformat()
        }

        collection_ref.add(data)

        print("Uploaded:", data, "\n")
        time.sleep(1)

    except Exception as e:
        print("Error:", e)
        time.sleep(2)
