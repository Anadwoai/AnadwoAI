import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
import requests, urllib.parse, re, os, time
from io import BytesIO
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

st.set_page_config(page_title="Anadwo - Any Story Fliki", page_icon="🎬", layout="centered")
st.title("🎬 Anadwo AI - Any Story → Fliki.ai")
st.caption("Type any story, get same quality as Abena's Hardest Week")

with st.sidebar:
    main_char = st.text_input("Main character lock", "19yo Ghanaian girl Abena short hair blue blouse same face")
    place = st.text_input("Place lock", "small poor room Tafo Kumasi Ghana, one bulb, wooden bed")
    seed = st.number_input("Face Seed (same = same person)", 4422)

story_input = st.text_area("Write ANY story here:", "My name is Kofi. I am 22 years old. I live in Accra. I lost my motorbike last week. I went to the police station. The officer said it will cost 2000 cedis. I had only 100 cedis. I cried all night.", height=150)

def plan_shot(sentence, char, place):
    s = sentence.lower()
    base = f"photorealistic cinematic, {char}, same person, {place}, 8k, vertical 9:16"
    if "my name is" in s or "i am" in s and len(s)<40:
        return f"{base}, standing in doorway of small room, looking at camera, title card, morning light"
    if "live" in s or "grandmother" in s or "mother" in s or "family" in s:
        return f"{base}, two people in small room talking, old grandmother with colorful headwrap on bed, young girl standing"
    if "left" in s or "window" in s or "accra" in s or "go" in s:
        return f"{base}, holding curtain looking out window, lonely, side profile"
    if "fell" in s or "sick" in s or "down" in s:
        return f"{base}, kneeling on floor helping old woman who fell, emotional"
    if "clinic" in s or "hospital" in s or "police" in s or "station" in s:
        return f"{base}, inside green clinic/police office in Ghana, helping old woman, fluorescent light"
    if "doctor" in s or "officer" in s or "said" in s:
        return f"{base}, Ghanaian official in uniform showing paper to young girl and old woman"
    if "cedis" in s or "money" in s or "thousand" in s or "cost" in s or "paper" in s or "bill" in s:
        return f"{base}, close up of paper / money / bill on wooden table, hands, clinic table"
    if "friday" in s or "before" in s or "calendar" in s or "time" in s:
        return f"{base}, wall calendar showing date circled in red, inside clinic"
    if "box" in s or "only" in s and "cedis" in s:
        return f"{base}, opening small wooden box with little money, close up hands on wooden table"
    if "cried" in s or "night" in s or "sad" in s:
        return f"{base}, sitting at wooden table crying, hands covering mouth, small box open"
    return f"{base}, scene: {sentence}"

def get_img(prompt, sd):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote_plus(prompt)}?width=720&height=1280&seed={sd}&model=flux&nologo=true&enhance=true"
    for _ in range(4):
        try:
            r = requests.get(url, timeout=70, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code==200 and len(r.content)>30000:
                return Image.open(BytesIO(r.content)).convert("RGB")
        except: pass
        time.sleep(3)
    return None

if st.button("🎬 GENERATE ANY STORY - FLIKI STYLE", type="primary", use_container_width=True):
    sentences = [s.strip() for s in re.split(r'[.\n]+', story_input) if len(s.strip())>8][:10]
    clips = []
    prog = st.progress(0)

    for i, sent in enumerate(sentences):
        prog.progress((i+1)/len(sentences))
        st.markdown(f"**Scene {i+1}: {sent}**")
        shot_prompt = plan_shot(sent, main_char, place)

        img = get_img(shot_prompt, int(seed)+i*4)
        if not img:
            st.warning("Server busy, retrying..."); time.sleep(4)
            img = get_img(shot_prompt, int(seed)+i*4+1)
        if not img: continue

        img_path = f"f_{i}.jpg"
        img.save(img_path)
        st.image(img, use_container_width=True)

        aud_path = f"a_{i}.mp3"
        gTTS(text=sent, lang='en', tld='com.ng').save(aud_path)

        # Video with yellow karaoke like your reference
        audio = AudioFileClip(aud_path)
        base = ImageClip(img_path).set_duration(audio.duration).resize(height=1280).set_audio(audio)

        # Create yellow subtitles chunks like Fliki
        words = sent.split()
        chunks = [" ".join(words[j:j+3]) for j in range(0, len(words), 3)]
        overlays = []
        durs = audio.duration / max(1, len(chunks))
        for c_idx, chunk in enumerate(chunks):
            sub = Image.new('RGBA', (720, 180), (0,0,0,0))
            draw = ImageDraw.Draw(sub)
            draw.text((20,30), chunk, fill="#FFEB3B", stroke_fill="black", stroke_width=4)
            p = f"s_{i}_{c_idx}.png"
            sub.save(p)
            overlays.append(ImageClip(p).set_start(c_idx*durs).set_duration(durs).set_pos(('center',0.80)))

        clips.append(CompositeVideoClip([base]+overlays, size=(720,1280)))
        st.audio(aud_path)
        st.divider()

    if clips:
        out = "Anadwo_AnyStory_Fliki.mp4"
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(out, fps=24, codec='libx264', audio_codec='aac')
        st.success("✅ Done! Same style as Abena video, any story!")
        st.video(out)
        with open(out, "rb") as f:
            st.download_button("⬇️ DOWNLOAD MP4", f, file_name=out, mime="video/mp4", use_container_width=True)
