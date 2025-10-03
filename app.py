import streamlit as st
import sounddevice as sd
import numpy as np
import tempfile
import wavio
import whisper
import requests
import time

st.title("🎙️ Real-time Scam Detector (Continuous)")

# Load Whisper once
@st.cache_resource
def load_whisper():
    return whisper.load_model("small")  # use "base" if PC is slower

whisper_model = load_whisper()

fs = 16000   # sampling frequency
chunk = 5    # seconds per recording chunk

# Session state to control loop
if "running" not in st.session_state:
    st.session_state.running = False

def start_recording():
    st.session_state.running = True

def stop_recording():
    st.session_state.running = False

col1, col2 = st.columns(2)
col1.button("🎤 Start", on_click=start_recording)
col2.button("⏹ Stop", on_click=stop_recording)

full_transcript = st.empty()
result_box = st.empty()

# Only run loop if "running" is True
while st.session_state.running:
    st.info("⏺️ Recording chunk...")
    recording = sd.rec(int(chunk * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()

    # Save temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wavio.write(temp_file.name, recording, fs, sampwidth=2)

    # --- Step 1: Transcribe ---
    result = whisper_model.transcribe(temp_file.name, language=None)
    transcript = result["text"].strip()

    # Store transcript in session
    if "transcript" not in st.session_state:
        st.session_state.transcript = ""
    st.session_state.transcript += " " + transcript

    # Update transcript display
    full_transcript.text_area("📝 Transcript so far:", st.session_state.transcript, height=150)

    # --- Step 2: Send to HF API ---
    try:
        response = requests.post(
            "https://st-thomas-of-aquinas-document-verification.hf.space/predict",
            json={"text": st.session_state.transcript}
        )

        if response.status_code == 200:
            prediction = response.json()
            result_box.subheader("🔎 Scam Detection (Live)")
            result_box.json(prediction)
        else:
            result_box.error(f"API Error: {response.status_code}")

    except Exception as e:
        result_box.error(f"Request failed: {e}")

    time.sleep(1)  # avoid overloading CPU
