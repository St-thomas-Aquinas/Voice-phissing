import streamlit as st
from st_audiorec import st_audiorec
import tempfile
import whisper

st.set_page_config(page_title="🎙️ Scam Detector", layout="centered")

st.title("🎙️ AI Scam Detector")
st.write("Record your voice and let the AI transcribe + analyze it in real time.")

# Load Whisper model (small for faster inference)
@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

# Audio recorder
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format="audio/wav")

    # Save audio to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with open(temp_file.name, "wb") as f:
        f.write(wav_audio_data)

    # Run Whisper transcription
    with st.spinner("Transcribing..."):
        result = model.transcribe(temp_file.name)
        transcript = result["text"]

    # Display result
    st.subheader("📝 Transcript")
    st.write(transcript)

    # Fake scam detection (replace with your ML/API later)
    if "bank" in transcript.lower() or "password" in transcript.lower():
        st.error("⚠️ Potential Scam Detected!")
    else:
        st.success("✅ Safe conversation")
