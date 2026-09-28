import streamlit as st
from gtts import gTTS
from PIL import Image
import requests
from io import BytesIO
import time

st.set_page_config(page_title="Anadwo AI", page_icon="🌙")
st.title("🌙 Anadwo AI - Text to Video (Ghana)")
story = st.text_area("Write your Ghana story:", "Abena was a brave girl in Kumasi who found a magical calabash under a baobab tree...", height=150)
if st.button("🎬 Generate Video Story", type="primary"):
    sentences = [s.strip() for s in story.split('.') if s.strip()][:4]
    st.info(f"Creating {len(sentences)} scenes...")
    for i, sentence in enumerate(sentences):
        st.subheader(f"Scene {i+1}: {sentence}")
        prompt = f"ghanaian children's storybook illustration, {sentence}, vibrant colors, african art"
        url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
        try:
            resp = requests.get(url, timeout=20)
            img = Image.open(BytesIO(resp.content))
            st.image(img, use_column_width=True)
        except:
            st.warning("Image failed")
        try:
            tts = gTTS(text=sentence, lang='en', tld='com.ng')
            tts.save(f"scene_{i}.mp3")
            st.audio(f"scene_{i}.mp3")
        except:
            st.error("Voice failed")
        time.sleep(1)
    st.success("✅ Anadwo Story Complete!")
    st.balloons()
