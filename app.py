import streamlit as st
from streamlit_audio_recorder import audio_recorder
import tempfile
import whisper

st.set_page_config(page_title="🎙️ Scam Detector", layout="centered")

st.title("🎙️ AI Scam Detector")
st.write("Record your voice, transcribe it with Whisper, and analyze for scams.")

# Load Whisper model (small = faster, medium/large = more accurate)
@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

# Audio recorder (records until user presses stop)
audio_bytes = audio_recorder(pause_threshold=30.0)

if audio_bytes:
    # Play back audio
    st.audio(audio_bytes, format="audio/wav")

    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file.write(audio_bytes)
    temp_file.flush()

    # Run Whisper transcription
    with st.spinner("Transcribing..."):
        result = model.transcribe(temp_file.name)
        transcript = result["text"]

    # Show transcript
    st.subheader("📝 Transcript")
    st.write(transcript)

    # 🚧 Replace this with your Hugging Face API call later
    if any(word in transcript.lower() for word in ["bank", "password", "mpesa", "pin", "account"]):
        st.error("⚠️ Potential Scam Detected!")
    else:
        st.success("✅ Safe conversation")
