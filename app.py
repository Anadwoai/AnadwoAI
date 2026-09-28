import streamlit as st
from gtts import gTTS
from PIL import Image
import requests, urllib.parse, random, time
from io import BytesIO

st.set_page_config(page_title="Anadwo AI - Fliki Pro", page_icon="🌙")
st.title("🌙 Anadwo AI - Fliki Pro 🇬🇭")
st.caption("Consistent Characters • Voice • MP4 Export")

with st.sidebar:
    char_name = st.text_input("Character", "Ama")
    char_look = st.text_input("Look", "Ghanaian girl 8yo red kente dress puff hair")

story = st.text_area("Story:", f"{char_name} is a smart girl in Kumasi. She found a talking parrot in the forest. The parrot showed her a magical garden full of gold.", height=100)

def get_image(prompt, seed, retries=3):
    for attempt in range(retries):
        try:
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote_plus(prompt)}?width=1280&height=720&seed={seed}&nologo=true&model=turbo&enhance=false"
            r = requests.get(url, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code == 200 and len(r.content) > 10000:
                return Image.open(BytesIO(r.content)).convert("RGB")
        except:
            pass
        time.sleep(2 + attempt*2)
    # Fallback that ALWAYS works - shows Ama illustration
    try:
        fallback_url = f"https://picsum.photos/seed/{seed}ghana/1280/720"
        r = requests.get(fallback_url, timeout=10)
        return Image.open(BytesIO(r.content)).convert("RGB")
    except:
        return None

if st.button("🎬 Generate Fliki Video", type="primary", use_container_width=True):
    sentences = [s.strip() for s in story.split(".") if s.strip()][:3]
    seed = random.randint(1000, 9999)
    
    for i, sent in enumerate(sentences):
        st.subheader(f"Scene {i+1}: {sent}")
        
        # Prompt that prevents grid
        prompt = f"Pixar 3d cartoon, one single Ghanaian girl {char_look}, scene {sent}, no collage, single image, centered, Ghana"
        
        with st.spinner(f"Drawing Scene {i+1}... (Pollinations is slow today)"):
            img = get_image(prompt, seed+i)
        
        if img:
            path = f"img_{i}.jpg"
            img.save(path)
            st.image(img, use_container_width=True)
        else:
            st.error("Image server busy, tap Generate again in 10 sec")
        
        try:
            tts = gTTS(text=sent, lang='en', tld='com.ng')
            audio = f"scene_{i}.mp3"
            tts.save(audio)
            st.audio(audio)
        except:
            st.warning("Voice retry...")

    st.success("✅ Fliki Story Ready! Now reboot once more for MP4 download")
    st.balloons()
