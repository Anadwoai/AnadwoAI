import streamlit as st
from gtts import gTTS
import tempfile

st.set_page_config(page_title="Anadwo AI", page_icon="🌙")
st.title("🌙 Anadwo AI")
st.caption("Fliki.ai for Ghana - Text to Video + Twi Voice")
st.markdown("---")

story = st.text_area("📝 Paste your Anadwo story:", height=200, placeholder="My name is Abena, 19 years old, from Tafo Kumasi... I am about to make the biggest mistake of my life...")

col1, col2 = st.columns(2)
with col1:
    voice = st.selectbox("🎙️ Voice", ["English Female", "Twi Accent"])
with col2:
    plan = st.selectbox("Plan", ["Free (Watermark)", "Premium 25 GHS"])

if st.button("🚀 Generate Audio Story", type="primary"):
    if not story:
        st.error("Paste story first!")
    else:
        with st.spinner("Anadwo AI is creating..."):
            tts = gTTS(text=story[:3500], lang='en', slow=False)
            audio_path = tempfile.mktemp(suffix=".mp3")
            tts.save(audio_path)
            st.success("✅ Your Anadwo Audio is Ready!")
            st.audio(audio_path)
            st.download_button("📥 Download MP3", open(audio_path,"rb").read(), file_name="Anadwo_AI.mp3", mime="audio/mp3")
            st.balloons()

st.markdown("---")
st.write("💰 **Make money:** Free users see watermark. Premium unlocks HD.")
st.link_button("Subscribe 25 GHS with MoMo (Paystack)", "https://paystack.com")
