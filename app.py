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
st.caption("Fliki.ai for Ghana - Built in Kumasi 🇬🇭")

story = st.text_area("Write your Ghana story:", "Ama is a smart girl in Kumasi. She found a talking parrot in the forest. The parrot showed her a hidden garden full of gold.", height=100)

if st.button("🎬 Generate Video Story", type="primary"):
    sentences = [s.strip() for s in story.split(".") if s.strip()][:4]
    if not sentences:
        st.error("Write a story first!")
    else:
        st.info(f"Creating {len(sentences)} scenes...")

        for i, sentence in enumerate(sentences):
            st.subheader(f"Scene {i+1}: {sentence}")
            
            # --- IMAGE ---
            prompt = f"ghanaian children's storybook illustration, {sentence}, vibrant colors, african art, cute"
            safe = urllib.parse.quote_plus(prompt)
            url = f"https://image.pollinations.ai/prompt/{safe}?width=1024&height=768&nologo=true&model=turbo&seed={random.randint(1,99999)}"
            
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                resp = requests.get(url, timeout=45, headers=headers)
                if resp.status_code == 200 and len(resp.content) > 1000:
                    img = Image.open(BytesIO(resp.content))
                    st.image(img, use_column_width=True)
                else:
                    raise Exception("Pollinations blocked")
            except Exception as e:
                st.caption(f"Using placeholder (Pollinations busy): {e}")
                # Fallback - will ALWAYS show image
                fallback_url = f"https://picsum.photos/seed/anadwo{i}{random.randint(1,9999)}/1024/768"
                st.image(fallback_url, use_column_width=True, caption="AI Illustration Placeholder")

            # --- VOICE ---
            try:
                tts = gTTS(text=sentence
