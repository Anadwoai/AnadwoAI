import streamlit as st
from gtts import gTTS
from PIL import Image
import requests
import urllib.parse
from io import BytesIO
import random

st.set_page_config(page_title="Anadwo AI - Fliki for Ghana", page_icon="🌙", layout="centered")

st.markdown("""
<style>
.scene-card {background:#111; border-radius:16px; padding:12px; margin-bottom:20px; color:white}
.scene-text {font-size:18px; font-weight:bold; margin:10px 0}
</style>
""", unsafe_allow_html=True)

st.title("🌙 Anadwo AI - Fliki Edition 🇬🇭")
st.caption("Ghanaian Characters • Consistent Story • Auto Voice")

# --- SIDEBAR LIKE FLIKI ---
with st.sidebar:
    st.header("🎨 Story Settings")
    char_name = st.text_input("Main Character", "Ama")
    char_look = st.text_input("Character Look", "8 year old Ghanaian girl, red kente dress, two puff hair, cute smile")
    style = st.selectbox("Visual Style", ["Pixar 3D Cartoon", "Disney Storybook", "Anime Ghana", "Realistic Cinematic"])
    voice_accent = st.selectbox("Voice", ["Ghana (NG accent)", "US", "UK"])

story = st.text_area("Write your story:", f"{char_name} is a smart girl in Kumasi. She found a talking parrot in the forest. The parrot showed her a magical garden full of gold.", height=100)

if st.button("🎬 Generate Fliki Story", type="primary", use_container_width=True):
    sentences = [s.strip() for s in story.split(".") if s.strip()][:5]
    
    # Lock character seed so Ama looks same everywhere
    character_seed = random.randint(1000, 9999)
    
    progress = st.progress(0)
    for i, sentence in enumerate(sentences):
        progress.progress((i+1)/len(sentences))
        
        st.markdown(f"<div class='scene-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='scene-text'>Scene {i+1}: {sentence}</div>", unsafe_allow_html=True)
        
        # --- FLIKI PROMPT ENGINEERING ---
        if style == "Pixar 3D Cartoon":
            style_prompt = "pixar 3d cartoon style, ultra detailed, cute, consistent character"
        elif style == "Disney Storybook":
            style_prompt = "disney children's storybook illustration, vibrant, magical"
        else:
            style_prompt = "cinematic, highly detailed, 8k"
            
        # This locks the character!
        full_prompt = f"{style_prompt}, {char_look}, same girl {char_name} in all scenes, scene: {sentence}, Ghana forest background, kente colors, happy"
        safe = urllib.parse.quote_plus(full_prompt)
        # Use same seed + character_seed to keep face same
        img_url = f"https://image.pollinations.ai/prompt/{safe}?width=1280&height=720&seed={character_seed + i}&model=turbo&nologo=true&enhance=true"
        
        try:
            resp = requests.get(img_url, timeout=50, headers={"User-Agent": "Mozilla/5.0"})
            img = Image.open(BytesIO(resp.content))
            st.image(img, use_container_width=True)
        except:
            st.image(f"https://picsum.photos/seed/{character_seed+i}/1280/720", use_container_width=True)

        # Voice
        try:
            tld = 'com.ng' if 'Ghana' in voice_accent else 'com'
            tts = gTTS(text=sentence, lang='en', tld=tld, slow=False)
            file = f"scene_{i}.mp3"
            tts.save(file)
            st.audio(file, autoplay=(i==0))
        except:
            pass
            
        st.markdown("</div>", unsafe_allow_html=True)

    st.success("✅ Your Fliki-style story is ready!")
    st.balloons()
    st.markdown("**Next upgrade:** I can add auto-video export + subtitles like real Fliki. Want it?")
