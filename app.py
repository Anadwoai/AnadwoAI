import streamlit as st
from gtts import gTTS
from PIL import Image
import requests, urllib.parse, random, os
from io import BytesIO

# For video export
try:
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
    MOVIEPY = True
except:
    MOVIEPY = False

st.set_page_config(page_title="Anadwo AI - Fliki Pro", page_icon="🌙", layout="centered")

st.title("🌙 Anadwo AI - Fliki Pro 🇬🇭")
st.caption("Consistent Characters • Voice • MP4 Video Export")

with st.sidebar:
    st.header("🎨 Settings")
    char_name = st.text_input("Character", "Ama")
    char_look = st.text_input("Look", "Ghanaian girl, 8yo, red kente dress, puff hair, cute")
    style = st.selectbox("Style", ["Pixar 3D", "Disney Storybook", "Anime"])

story = st.text_area("Story:", f"{char_name} is a smart girl in Kumasi. She found a talking parrot in the forest. The parrot showed her a magical garden full of gold.", height=100)

if st.button("🎬 Generate Fliki Video", type="primary", use_container_width=True):
    sentences = [s.strip() for s in story.split(".") if s.strip()][:4]
    seed = random.randint(1000, 9999)
    
    images, audios = [], []
    
    for i, sent in enumerate(sentences):
        st.subheader(f"Scene {i+1}: {sent}")
        
        # FIXED prompt - prevents 4-grid
        prompt = f"single character, one girl only, {style} style, {char_look}, same face, {sent}, Ghana background, no collage, no grid, portrait"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote_plus(prompt)}?width=1280&height=720&seed={seed+i}&nologo=true&model=turbo"
        
        try:
            r = requests.get(url, timeout=50, headers={"User-Agent":"Mozilla/5.0"})
            img = Image.open(BytesIO(r.content)).convert("RGB")
            img_path = f"img_{i}.jpg"
            img.save(img_path)
            images.append(img_path)
            st.image(img, use_container_width=True)
        except:
            st.warning("Image busy, retry")

        # Voice
        try:
            tts = gTTS(text=sent, lang='en', tld='com.ng')
            audio_path = f"scene_{i}.mp3"
            tts.save(audio_path)
            audios.append(audio_path)
            st.audio(audio_path)
        except:
            pass

    # --- CREATE MP4 LIKE FLIKI ---
    if MOVIEPY and images and audios and len(images)==len(audios):
        st.info("🎞️ Creating Fliki video...")
        clips = []
        for img_path, audio_path in zip(images, audios):
            audio = AudioFileClip(audio_path)
            clip = ImageClip(img_path).set_duration(audio.duration).set_audio(audio)
            # Add subtitle text like Fliki
            try:
                txt = TextClip(sentences[len(clips)], fontsize=40, color='white', bg_color='black', size=(1000, None), method='caption').set_duration(audio.duration).set_position(('center','bottom'))
                clip = CompositeVideoClip([clip.resize((1280,720)), txt])
            except:
                clip = clip.resize((1280,720))
            clips.append(clip)
        
        final = concatenate_videoclips(clips)
        final.write_videofile("anadwo_story.mp4", fps=24, codec='libx264', audio_codec='aac')
        st.success("✅ Fliki Video Ready!")
        st.video("anadwo_story.mp4")
        with open("anadwo_story.mp4", "rb") as f:
            st.download_button("⬇️ Download MP4 (Fliki Style)", f, "Anadwo_Story.mp4", "video/mp4", use_container_width=True)
    else:
        st.success("✅ Story ready! Add to requirements.txt: moviepy")
        st.code("moviepy\nPillow\nrequests\ngTTS\nstreamlit")

st.markdown("---")
st.caption("Built in Kumasi 🇬🇭 | requirements.txt needs: streamlit, gTTS, Pillow, requests, moviepy, imageio-ffmpeg")
