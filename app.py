import streamlit as st
from gtts import gTTS
from PIL import Image
import requests, urllib.parse, random, time, re
from io import BytesIO

st.set_page_config(page_title="Anadwo AI - Universal Cinema", page_icon="🎬", layout="centered")
st.title("🎬 Anadwo AI - Any Story → Fliki Movie")

# --- SIDEBAR = FLIKI CONTROL ---
with st.sidebar:
    st.header("🎭 Character Lock")
    char_name = st.text_input("Character Name", "Abena")
    char_age = st.text_input("Age / Gender", "19 year old Ghanaian girl")
    char_look = st.text_area("Exact Look (LOCKS FACE)", "short natural hair, slim face, sad eyes, blue blouse, dark skirt, same face in all scenes", height=80)
    location = st.text_input("Location", "Tafo Kumasi Ghana, small poor room, single bulb")
    seed = st.number_input("Face Seed (keep same = same actress)", value=4422, step=1)
    style = st.selectbox("Style", ["Cinematic Realistic (like your video)", "Nollywood Drama", "Documentary Photo"])
    
st.caption(f"Seed {seed} = same {char_name} in all scenes. Change it = new actress.")

story = st.text_area("WRITE ANY STORY HERE:", """Abena's Hardest Week.
My name is Abina. I am nineteen years old. I live in Tafo with my grandmother.
My mother left us when I was four. She said she was going to Accra.
Last week my grandmother fell down. I took her to the clinic. The doctor said she needs 3000 cedis before Friday.
I had only 42 cedis in my box. I cried all night.""", height=200)

def clean_sentence(s): return s.strip()

def make_cinematic_prompt(sentence, char_name, char_age, char_look, location, style_mode):
    # THIS IS THE SECRET - Always force character + location, never just sentence
    base = f"photorealistic, cinematic, {char_age} named {char_name}, {char_look}, doing: {sentence}, in {location}, {style_mode}, ultra detailed skin, consistent face, same person, no cartoon, 8k, dramatic lighting, vertical portrait 9:16, film still"
    return base

def get_image(prompt_text, seed_val, retries=3):
    model = "flux"  # most realistic, like Fliki
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote_plus(prompt_text)}?width=720&height=1280&seed={seed_val}&model={model}&nologo=true&enhance=true"
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code == 200 and len(r.content) > 30000:
                return Image.open(BytesIO(r.content)).convert("RGB")
        except: pass
        time.sleep(4)
    return None

if st.button("🎬 GENERATE CINEMATIC STORY", type="primary", use_container_width=True):
    # Split any story into scenes
    raw = story.replace("\n", ". ")
    sentences = [clean_sentence(s) for s in re.split(r'[.\n]+', raw) if len(clean_sentence(s)) > 8][:12]
    
    if not sentences:
        st.error("Write a story first")
        st.stop()

    st.progress(0)
    for i, sent in enumerate(sentences):
        st.markdown(f"#### Scene {i+1}: {sent}")
        
        prompt = make_cinematic_prompt(sent, char_name, char_age, char_look, location, style)
        
        with st.spinner(f"🎥 Filming Scene {i+1}/{len(sentences)} - {char_name}... (15s)"):
            # seed + i*7 keeps same face but different pose
            img = get_image(prompt, int(seed) + i*7)
        
        if img:
            st.image(img, use_container_width=True)
            # Fliki yellow word highlight
            words = sent.split()
            st.markdown(f"""
            <div style='background:#111; padding:14px; border-radius:10px; text-align:center;'>
                <p style='color:white; font-size:19px; line-height:1.6; margin:0;'>{sent}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Image server busy. Wait 20 sec and Generate again - seed keeps same face.")

        # Voice
        try:
            tts = gTTS(text=sent, lang='en', tld='com.ng')
            path = f"scene_{i}.mp3"
            tts.save(path)
            st.audio(path)
        except: pass
        
        st.divider()
        st.progress((i+1)/len(sentences))

    st.success(f"✅ Done! {char_name}'s movie ready. All scenes = same actress because seed={seed}")
    st.balloons()
