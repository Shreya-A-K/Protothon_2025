# app.py
import streamlit as st
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore
import plotly.express as px
import requests
import os
import json
from datetime import datetime

# -------------------------------
# Firebase setup (SAFE VERSION)
# -------------------------------
# Load credentials from environment variable path
SERVICE_KEY_PATH = os.getenv("FIREBASE_KEY", "serviceAccountKey.json")

cred = credentials.Certificate(SERVICE_KEY_PATH)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

DEVICE_ID = "master01"

# -------------------------------
# Telegram setup (SAFE VERSION)
# -------------------------------
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "").split(",")  # comma-separated list

def send_telegram_alert(message):
    if not BOT_TOKEN or CHAT_IDS == [""]:
        print("Telegram credentials not configured. Skipping alert.")
        return

    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print("Telegram send error:", e)

# -------------------------------
# Streamlit sidebar: thresholds
# -------------------------------
st.sidebar.subheader("Anomaly Detection Settings")
temp_warning = st.sidebar.number_input("Warning Temperature", value=70.0)
moist_warning = st.sidebar.number_input("Warning Moisture", value=800.0)
temp_critical = st.sidebar.number_input("Critical Temperature", value=100.0)
moist_critical = st.sidebar.number_input("Critical Moisture", value=1000.0)
send_alerts = st.sidebar.checkbox("Send Telegram Alerts", value=True)

# -------------------------------
# Fetch Firestore telemetry
# -------------------------------
@st.cache_data(ttl=60)
def fetch_telemetry():
    docs = db.collection("SensorReadings").stream()
    rows = []
    for doc in docs:
        d = doc.to_dict()
        rows.append({
            "timestamp": pd.to_datetime(d["timestamp"]),
            "temp_1": float(d["temperature"]),
            "moist_1": float(d["humidity"])
        })
    if rows:
        df = pd.DataFrame(rows).sort_values("timestamp").reset_index(drop=True)
    else:
        df = pd.DataFrame(columns=["timestamp","temp_1","moist_1"])
    return df

# -------------------------------
# Detect anomalies
# -------------------------------
def generate_alert_message(temp, moist, severity):
    if severity == "critical":
        return f"⚠️ *Critical Alert!*\nTemp: {temp}\nMoist: {moist}\nCheck system immediately."
    elif severity == "warning":
        return f"⚠️ Warning: Temp: {temp}, Moist: {moist}. Abnormal reading."
    return "Normal"

def detect_anomalies_threshold(df, temp_warning, moist_warning, temp_critical, moist_critical, send_alerts=True):
    df["severity"] = "normal"
    df.loc[(df.temp_1 >= temp_warning) | (df.moist_1 >= moist_warning), "severity"] = "warning"
    df.loc[(df.temp_1 >= temp_critical) | (df.moist_1 >= moist_critical), "severity"] = "critical"

    df["message"] = df.apply(lambda row: generate_alert_message(row["temp_1"], row["moist_1"], row["severity"]), axis=1)

    if send_alerts:
        anomalies = df[df.severity != "normal"]
        for _, row in anomalies.iterrows():
            send_telegram_alert(row["message"])

    return df

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="IoT Dashboard", layout="wide")
st.title("Protothon IoT Dashboard")

df = fetch_telemetry()
st.subheader(f"Telemetry fetched: {len(df)} samples")

if len(df) < 1:
    st.warning("No telemetry data found.")
else:
    df_anom = detect_anomalies_threshold(df, temp_warning, moist_warning, temp_critical, moist_critical, send_alerts)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total samples", len(df_anom))
    col2.metric("Anomalies", df_anom[df_anom.severity!="normal"].shape[0])
    col3.metric("Latest temp", f"{df_anom.iloc[-1]['temp_1']:.2f}")
    col4.metric("Latest moist", f"{df_anom.iloc[-1]['moist_1']:.2f}")

    st.subheader("Telemetry Over Time")
    fig = px.line(df_anom, x="timestamp", y=["temp_1","moist_1"])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Anomalies Detected")
    st.dataframe(df_anom[df_anom.severity!="normal"][["timestamp","temp_1","moist_1","severity","message"]])

    st.subheader("Full Telemetry Data")
    st.dataframe(df_anom.sort_values("timestamp", ascending=False))
