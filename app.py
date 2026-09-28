import streamlit as st
from gtts import gTTS
from PIL import Image
import requests, os, re
import tempfile
from io import BytesIO
from moviepy.editor import *

st.set_page_config(
 page_title="Anadwo AI",
 page_icon="🌙")

st.title("🌙 Anadwo AI")
st.write("Text to Video")

story = st.text_area(
 "Story",
 "My name is Abena from Tafo Kumasi. I am about to make the biggest mistake of my life.",
 height=100)

def get_img(p):
 short = p[:20]
 base = "https://image.pollinations.ai/prompt/"
 url = base + short + " Ghana girl"
 try:
  r = requests.get(url, timeout=20)
  return Image.open(BytesIO(r.content))
 except:
  return Image.new(
   'RGB',(720,1280),
   color=(15,15,30))

def split_t(t):
 s = re.split(r'[.!?]+', t)
 out = []
 for x in s:
  if len(x.strip())>10:
   out.append(x.strip())
 return out[:5]

if st.button("Generate Video"):
 sents = split_t(story)
 st.info(f"Making {len(sents)} scenes")
 tmp = tempfile.mkdtemp()
 clips = []
 bar = st.progress(0)
 for i, sent in enumerate(sents):
  bar.progress((i+1)/len(sents))
  ap = os.path.join(tmp, f"a{i}.mp3")
  gTTS(text=sent, lang="en").save(ap)
  img = get_img(sent)
  ip = os.path.join(tmp, f"i{i}.jpg")
  img.save(ip)
  ac = AudioFileClip(ap)
  ic = ImageClip(ip)
  ic = ic.set_duration(
   ac.duration+0.5)
  ic = ic.set_audio(ac)
  ic = ic.resize(height=720)
  clips.append(ic)
 final = concatenate_videoclips(
  clips, method="compose")
 out = os.path.join(tmp, "v.mp4")
 final.write_videofile(
  out, fps=24,
  codec='libx264',
  audio_codec='aac',
  logger=None)
 st.success("Ready!")
 st.video(out)
 with open(out,"rb") as f:
  st.download_button(
   "Download MP4",
   f,
   file_name="anadwo.mp4")
