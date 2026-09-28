import streamlit as st
from gtts import gTTS
from PIL import Image
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
import requests, urllib.parse, re, time
from io import BytesIO
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

st.set_page_config(page_title="AnadwoAI", layout="centered")
st.title("ANADWOAI - Script to Video")
st.write("Type any story. We make video with voice + images like Fliki.")

story = st.text_area("Your script", "My name is Kofi. I am 22 years old. I live in Accra. I lost my motorbike last week. I went to the police station. I had only 100 cedis.", height=120)
seed = st.number_input("Seed (keep same to keep same face)", value=4422)

def make_image(prompt, s):
    url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote_plus(prompt) + "?width=720&height=1280&seed=" + str(s) + "&model=flux&nologo=true"
    try:
        r = requests.get(url, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code == 200:
            return Image.open(BytesIO(r.content)).convert("RGB")
    except:
        return None
    return None

if st.button("GENERATE VIDEO", type="primary", use_container_width=True):
    lines = [x.strip() for x in re.split(r'[.\n]+', story) if len(x.strip()) > 5][:5]
    video_parts = []
    for i, line in enumerate(lines):
        st.write(f"Scene {i+1}: {line}")
        p = f"photorealistic, cinematic, ghanaian, consistent character, scene: {line}, 8k"
        img = make_image(p, int(seed)+i*3)
        if img is None:
            st.warning("Image server busy, skipping scene")
            continue
        img_path = f"img_{i}.jpg"
        img.save(img_path)
        st.image(img, use_container_width=True)
        audio_path = f"aud_{i}.mp3"
        gTTS(text=line, lang='en', tld='com.ng').save(audio_path)
        audio = AudioFileClip(audio_path)
        clip = ImageClip(img_path).set_duration(audio.duration).set_audio(audio).resize(height=720)
        video_parts.append(clip)
        time.sleep(1)

    if video_parts:
        final_path = "AnadwoAI_video.mp4"
        final = concatenate_videoclips(video_parts, method="compose")
        final.write_videofile(final_path, fps=24, codec='libx264', audio_codec='aac')
        st.success("Done! Your video is ready")
        st.video(final_path)
        with open(final_path, "rb") as f:
            st.download_button("Download MP4", f, file_name=final_path, mime="video/mp4", use_container_width=True)
    else:
        st.error("No images generated, try again")
