import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
import requests, urllib.parse, re, os, time
from io import BytesIO
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

st.set_page_config(page_title="AnadwoAI", page_icon="A", layout="centered")
st.title("ANADWOAI.COM")
st.caption("Ghana's Fliki - Any story to video")

story = st.text_area("Write ANY story here:", "My name is Kofi. I am 22 years old. I live in Accra. I lost my motorbike last week. I went to the police station. The officer said it will cost 2000 cedis. I had only 100 cedis. I cried all night.", height=150)

seed = st.number_input("Face Seed (same = same person)", value=4422)

def get_img(prompt, sd):
    url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote_plus(prompt) + "?width=720&height=1280&seed=" + str(sd) + "&model=flux&nologo=true"
    for _ in range(3):
        try:
            r = requests.get(url, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code == 200 and len(r.content) > 25000:
                return Image.open(BytesIO(r.content)).convert("RGB")
        except:
            pass
        time.sleep(2)
    return None

if st.button("GENERATE ANY STORY - FLIKI STYLE", type="primary", use_container_width=True):
    sentences = [s.strip() for s in re.split(r'[.\n]+', story) if len(s.strip()) > 8][:6]
    clips = []
    prog = st.progress(0)
    
    for i, sent in enumerate(sentences):
        prog.progress((i + 1) / len(sentences))
        st.write(f"Scene {i+1}: {sent}")
        
        prompt = f"photorealistic cinematic, Ghanaian person, same face, consistent, scene {sent}, 8k vertical 9:16"
        img = get_img(prompt, int(seed) + i*4)
        
        if img is None:
            st.warning("Retrying image")
            continue
            
        img_path = f"ana_{i}.jpg"
        img.save(img_path)
        st.image(img, use_container_width=True)
        
        aud_path = f"ana_{i}.mp3"
        gTTS(text=sent, lang='en', tld='com.ng').save(aud_path)
        st.audio(aud_path)
        
        try:
            audio = AudioFileClip(aud_path)
            base = ImageClip(img_path).set_duration(audio.duration).resize(height=1280).set_audio(audio)
            sub = Image.new('RGBA', (720, 120), (0,0,0,0))
            draw = ImageDraw.Draw(sub)
            draw.text((20,20), sent[:50], fill="yellow", stroke_fill="black", stroke_width=3)
            sp = f"sub_{i}.png"
            sub.save(sp)
            overlay = ImageClip(sp).set_duration(audio.duration).set_pos(('center', 0.8))
            final = CompositeVideoClip([base, overlay], size=(720,1280))
            clips.append(final)
        except Exception as e:
            st.write(e)
    
    if clips:
        out = "AnadwoAI_Video.mp4"
        final_video = concatenate_videoclips(clips, method="compose")
        final_video
