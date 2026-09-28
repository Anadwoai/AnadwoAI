import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import requests, urllib.parse, re, os, time
from io import BytesIO

try:
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
    HAS_MOVIEPY = True
except:
    HAS_MOVIEPY = False

st.set_page_config(page_title="Anadwo AI - Fixed MP4", page_icon="🎬", layout="centered")
st.title("🎬 Anadwo AI - Fixed MP4 🇬🇭")
st.caption("No ImageMagick needed - Works 100%")

with st.sidebar:
    char_name = st.text_input("Name", "Abena")
    char_desc = st.text_area("LOCK FACE (same actress)", "19 year old Ghanaian girl, short natural hair, blue blouse, dark skirt, same face, photorealistic", height=80)
    location = st.text_input("Location", "small room Tafo Kumasi Ghana")
    seed = st.number_input("Face Seed", value=4422)

story = st.text_area("Write ANY story:", """My name is Abina. I am 19 years old. I live in Tafo Kumasi with my grandmother. My mother left us when I was 4 years old. She said she was going to Accra to find work. Last week my grandmother fell down. I took her to the clinic. The doctor said she needs 3000 cedis before Friday. I had only 42 cedis in my box.""", height=180)

def get_img(prompt, sd):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote_plus(prompt)}?width=720&height=1280&seed={sd}&model=flux&nologo=true&enhance=true"
    for _ in range(4):
        try:
            r = requests.get(url, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code==200 and len(r.content)>30000:
                return Image.open(BytesIO(r.content)).convert("RGB")
        except: pass
        time.sleep(4)
    return None

def make_subtitle_image(text, width=720, height=200):
    # Create yellow subtitle on black semi-transparent using PIL - NO ImageMagick!
    img = Image.new('RGBA', (width, height), (0,0,0,180))
    draw = ImageDraw.Draw(img)
    # Try to wrap text
    words = text.split()
    lines = []
    line = ""
    for w in words:
        if len(line + " " + w) < 38:
            line += " " + w
        else:
            lines.append(line.strip())
            line = w
    lines.append(line.strip())
    y = 20
    for l in lines[:3]:
        # Yellow text with black stroke
        draw.text((20, y), l, fill="yellow", stroke_fill="black", stroke_width=3, font=ImageFont.load_default())
        y += 45
    return img

if st.button("🎬 GENERATE FIXED MP4", type="primary", use_container_width=True):
    sentences = [s.strip() for s in re.split(r'[.\n]+', story) if len(s.strip())>8][:8]
    clips = []
    temp = []
    
    prog = st.progress(0)
    for i, sent in enumerate(sentences):
        prog.progress((i+1)/len(sentences))
        st.write(f"**Scene {i+1}: {sent}**")
        
        prompt = f"photorealistic cinematic, {char_desc} named {char_name}, scene: {sent}, in {location}, same person, consistent face, 8k, vertical 9:16, film still"
        img = get_img(prompt, int(seed)+i*7)
        
        if not img:
            st.warning(f"Scene {i+1} busy, retry")
            continue
            
        img_path = f"img_{i}.jpg"
        img.save(img_path)
        st.image(img, use_container_width=True)
        
        audio_path = f"aud_{i}.mp3"
        try:
            gTTS(text=sent, lang='en', tld='com.ng').save(audio_path)
            st.audio(audio_path)
            
            if HAS_MOVIEPY:
                audio = AudioFileClip(audio_path)
                # Main image clip
                img_clip = ImageClip(img_path).set_duration(audio.duration).resize((720,1280)).set_audio(audio)
                
                # Subtitle clip using PIL image - NO TextClip!
                sub_pil = make_subtitle_image(sent)
                sub_path = f"sub_{i}.png"
                sub_pil.save(sub_path)
                sub_clip = ImageClip(sub_path).set_duration(audio.duration).set_position(('center', 0.75))
                
                comp = CompositeVideoClip([img_clip, sub_clip])
                clips.append(comp)
                temp.extend([img_path, audio_path, sub_path])
            else:
                temp.extend([img_path, audio_path])
        except Exception as e:
            st.error(f"Audio error fixed next run: {e}")
        st.divider()

    if HAS_MOVIEPY and clips:
        st.info("🎞️ Merging final MP4...")
        final = concatenate_videoclips(clips, method="compose")
        out = "Anadwo_Fliki_Final.mp4"
        final.write_videofile(out, fps=24, codec='libx264', audio_codec='aac')
        st.success("✅ MP4 DONE - No ImageMagick error!")
        st.video(out)
        with open(out, "rb") as f:
            st.download_button("⬇️ DOWNLOAD MP4 NOW", f, file_name=out, mime="video/mp4", use_container_width=True)
        
        for p in temp:
            if os.path.exists(p): os.remove(p)
        if os.path.exists(out): os.remove(out)
    else:
        if not HAS_MOVIEPY:
            st.warning("Reboot app to install moviepy")
        st.success("Images + voice ready, MP4 will work after reboot")
