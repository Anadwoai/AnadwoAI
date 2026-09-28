import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw
import PIL.Image
# FIX for new Pillow - moviepy bug
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import requests, urllib.parse, re, os, time
from io import BytesIO

try:
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
    HAS_MOVIEPY = True
except:
    HAS_MOVIEPY = False

st.set_page_config(page_title="Anadwo AI - Final", page_icon="🎬", layout="centered")
st.title("🎬 Anadwo AI - Final Fixed MP4")

with st.sidebar:
    char_name = st.text_input("Name", "Abena")
    char_desc = st.text_area("LOCK FACE", "19 year old Ghanaian girl, short natural hair, blue blouse, same face, photorealistic", height=70)
    location = st.text_input("Location", "Tafo Kumasi Ghana small room")
    seed = st.number_input("Face Seed", value=4422)

story = st.text_area("Write ANY story:", "My name is Abina. I am 19 years old. I live in Tafo Kumasi with my grandmother. My mother left us when I was 4 years old. She said she was going to Accra to find work. Last week my grandmother fell down. I took her to the clinic. The doctor said she needs 3000 cedis before Friday. I had only 42 cedis in my box.", height=150)

def get_img(prompt, sd):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote_plus(prompt)}?width=720&height=1280&seed={sd}&model=flux&nologo=true&enhance=true"
    for _ in range(3):
        try:
            r = requests.get(url, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code==200 and len(r.content)>25000:
                return Image.open(BytesIO(r.content)).convert("RGB")
        except: pass
        time.sleep(3)
    return None

def make_subtitle_pil(text):
    # Black bar + yellow text - no ImageMagick
    img = Image.new('RGBA', (720, 180), (0,0,0,170))
    draw = ImageDraw.Draw(img)
    # simple wrap
    lines = []
    cur = ""
    for w in text.split():
        if len(cur + " " + w) < 35:
            cur += " " + w
        else:
            lines.append(cur.strip()); cur = w
    lines.append(cur.strip())
    y=15
    for l in lines[:3]:
        draw.text((15, y), l, fill="yellow", stroke_fill="black", stroke_width=2)
        y+=45
    return img

if st.button("🎬 GENERATE FINAL MP4 - FIXED", type="primary", use_container_width=True):
    sentences = [s.strip() for s in re.split(r'[.\n]+', story) if len(s.strip())>8][:6]
    clips = []
    files = []
    prog = st.progress(0)
    
    for i, sent in enumerate(sentences):
        prog.progress((i+1)/len(sentences))
        st.write(f"**Scene {i+1}: {sent}**")
        prompt = f"photorealistic cinematic, {char_desc} named {char_name}, scene: {sent}, in {location}, same person, 8k, vertical 9:16"
        img = get_img(prompt, int(seed)+i*7)
        if not img:
            st.warning("Busy - retry in 15s"); continue
        
        img_path = f"img_{i}.jpg"
        img.save(img_path)
        st.image(img, use_container_width=True)
        
        audio_path = f"aud_{i}.mp3"
        try:
            gTTS(text=sent, lang='en', tld='com.ng').save(audio_path)
            st.audio(audio_path)
            
            if HAS_MOVIEPY:
                audio = AudioFileClip(audio_path)
                # FIXED: don't use resize with ANTIALIAS, use with LANCZOS
                base_clip = ImageClip(img_path).set_duration(audio.duration)
                # Force resize using PIL not moviepy antialias
                base_clip = base_clip.resize(height=1280)
                base_clip = base_clip.set_audio(audio)
                
                sub_img = make_subtitle_pil(sent)
                sub_path = f"sub_{i}.png"
                sub_img.save(sub_path)
                sub_clip = ImageClip(sub_path).set_duration(audio.duration).set_pos(('center', 0.75))
                
                final_clip = CompositeVideoClip([base_clip, sub_clip], size=(720,1280))
                clips.append(final_clip)
                files += [img_path, audio_path, sub_path]
        except Exception as e:
            st.error(f"Error: {e}")
        st.divider()

    if HAS_MOVIEPY and clips:
        st.info("Merging MP4... 30 sec")
        try:
            out = "Anadwo_Final.mp4"
            concat = concatenate_videoclips(clips, method="compose")
            concat.write_videofile(out, fps=24, codec='libx264', audio_codec='aac')
            st.success("✅ MP4 READY - No more ANTIALIAS error!")
            st.video(out)
            with open(out, "rb") as f:
                st.download_button("⬇️ DOWNLOAD MP4", f, file_name=out, mime="video/mp4", use_container_width=True)
        except Exception as e:
            st.error(f"MP4 error: {e}")
    else:
        st.success("Images + audio done. If MP4 didn't show, Reboot once more.")
    
