import streamlit as st
from gtts import gTTS
from PIL import Image
import requests
import urllib.parse
from io import BytesIO
import time
import random

st.set_page_config(page_title="Anadwo AI", page_icon="🌙")
st.title("🌙 Anadwo AI - Text to Video (Ghana)")

story = st.text_area("Write your Ghana story:", "Ama is a smart girl in Kumasi. She found a talking parrot in the forest. The parrot showed her a hidden garden full of gold.")

if st.button("Generate Video Story", type="primary"):
    sentences = [s.strip() for s in story.split(".") if s.strip()][:4]
    st.info(f"Creating {len(sentences)} scenes...")
    for i, sentence in enumerate(sentences):
        st.subheader(f"Scene {i+1}: {sentence}")
        prompt = f"ghanaian childrens storybook illustration {sentence} vibrant colors african art cute"
        safe = urllib.parse.quote_plus(prompt)
        url = f"https://image.pollinations.ai/prompt/{safe}?width=1024&height=768&nologo=true&seed={random.randint(1,99999)}"
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, timeout=45, headers=headers)
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content))
                st.image(img, use_column_width=True)
            else:
                st.image(f"https://picsum.photos/seed/anadwo{i}/1024/768", use_column_width=True)
        except:
            st.image(f"https://picsum.photos/seed/anadwo{i}/1024/768", use_column_width=True)
        try:
            tts = gTTS(text=sentence, lang='en', tld='com.ng')
            tts.save(f"scene_{i}.mp3")
            st.audio(f"scene_{i}.mp3")
        except:
            st.error("Voice failed")
        time.sleep(0.5)
    st.success("Anadwo Story Complete!")
    st.balloons()
