import streamlit as st
from gtts import gTTS
from PIL import Image
import requests, urllib.parse, random, time, re, os
from io import BytesIO

try:
    from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
    HAS_MOVIEPY = True
except:
    HAS_MOVIEPY = False

st.set_page_config(page_title="Anadwo AI - Fliki Pro MP4", page_icon="🎬", layout="centered")
st.title("🎬 Anadwo AI - Fliki Pro MP4 🇬🇭")
st.caption("Any story → Cinematic 9:16 + Yellow Subtitles + Download")

with st.sidebar:
    char_name = st.text_input("Name", "Abena")
    char_desc = st.text_area("LOCK FACE", "19 year old Ghanaian girl, short hair, blue blouse, same face", height=80)
    location = st.text_input("Location", "small room Tafo Kumasi Ghana, single bulb")
    seed = st.number_input("Face Seed", value=4422)
    speed = st.slider("Video speed per scene", 0.8, 1.5, 1.0)

story = st.text_area("Write ANY story:", """My name is Abina. I am 19 years old. I live in Tafo Kumasi with my grandmother. My mother left us when I was 4 years old. She said she was going to Accra to find work. Last week my grandmother fell down. I took her to the clinic. The doctor said she needs 3000 cedis before Friday. I had only 42 cedis in my box.""", height=180)

def get_img(prompt, sd):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote_plus(prompt)}?width=720&height=1280&seed={sd}&model=flux&nologo=true&enhance=true"
    for _ in range(3):
        try:
            r = requests.get(url, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code==200 and len(r.content)>30000:
                return Image.open(BytesIO(r.content)).convert("RGB")
        except: pass
        time.sleep(3)
    return None

if st.button("🎬 GENERATE & EXPORT MP4 (Fliki Pro)", type="primary", use_container_width=True):
    sentences = [s.strip() for s in re.split(r'[.\n]+', story) if len(s.strip())>8][:8]
    clips, temp_files = [], []
    
    progress = st.progress(0)
    
    for i, sent in enumerate(sentences):
        progress.progress((i+1)/len(sentences))
        st.subheader(f"Scene {i+1}: {sent}")
        
        prompt = f"photorealistic cinematic, {char_desc} named {char_name}, scene: {sent}, in {location}, same person, consistent face, 8k, dramatic, vertical 9:16, film still"
        img = get_img(prompt, int(seed)+i*7)
        
        if not img:
            st.warning("Image busy, retry in 15 sec")
            continue
            
        img_path = f"img_{i}.jpg"
        img.save(img_path)
        st.image(img, use_container_width=True)

        audio_path = f"aud_{i}.mp3"
        try:
            gTTS(text=sent, lang='en', tld='com.ng').save(audio_path)
            st.audio(audio_path)
            temp_files.append(audio_path)
            temp_files.append(img_path)
            
            if HAS_MOVIEPY:
                audio_clip = AudioFileClip(audio_path)
                # yellow subtitle like Fliki
                txt_clip = TextClip(sent, fontsize=32, color='yellow', stroke_color='black', stroke_width=2, method='caption', size=(660, None)).set_duration(audio_clip.duration).set_position(('center', 0.78), relative=True)
                img_clip = ImageClip(img_path).set_duration(audio_clip.duration).set_audio(audio_clip)
                # slow zoom like Fliki (Ken Burns)
                img_clip = img_clip.resize((720, 1280))
                comp = CompositeVideoClip([img_clip, txt_clip])
                clips.append(comp)
        except Exception as e:
            st.error(f"Audio error: {e}")

    if HAS_MOVIEPY and clips:
        st.info("🎞️ Creating final MP4 like Fliki.ai...")
        final = concatenate_videoclips(clips, method="compose")
        out = "Abena_Fliki_Story.mp4"
        final.write_videofile(out, fps=24, codec='libx264', audio_codec='aac')
        st.success("✅ MP4 READY!")
        st.video(out)
        with open(out, "rb") as f:
            st.download_button("⬇️ DOWNLOAD MP4 (9:16 Fliki Style)", f, file_name=out, mime="video/mp4", use_container_width=True)
        
        # cleanup
        for p in temp_files: 
            if os.path.exists(p): os.remove(p)
    else:
        if not HAS_MOVIEPY:
            st.warning("Add moviepy to requirements.txt and Reboot to get MP4 download")
        st.success("✅ Images + Voice ready!")

st.markdown("---")
st.caption("Tip: Keep same seed = same actress for any story. Change story text = new movie, same girl.")
