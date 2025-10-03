import streamlit as st
from st_audiorec import st_audiorec   # ✅ correct library
import tempfile
import whisper

st.set_page_config(page_title="🎙️ Scam Detector", layout="centered")

st.title("🎙️ AI Scam Detector")
st.write("Record your voice, transcribe it with Whisper, and analyze for scams.")

# Load Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

# Record audio in browser
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format="audio/wav")

    # Save audio to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with open(temp_file.name, "wb") as f:
        f.write(wav_audio_data)

    # Transcribe with Whisper
    with st.spinner("Transcribing..."):
        result = model.transcribe(temp_file.name)
        transcript = result["text"]

    st.subheader("📝 Transcript")
    st.write(transcript)

    # Simple scam detection
    if any(word in transcript.lower() for word in ["bank", "password", "mpesa", "pin", "account"]):
        st.error("⚠️ Potential Scam Detected!")
    else:
        st.success("✅ Safe conversation")
