import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
import requests, urllib.parse, re, os, time
from io import BytesIO
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

st.set_page_config(page_title="AnadwoAI - Ghana's Fliki", page_icon="🎬", layout="centered")

# ===== ANADWOAI BRANDING CSS =====
st.markdown("""
<style>
header {visibility:hidden;}
.block-container {padding-top:0; padding-bottom:90px; max-width:420px; background:#FFF8FA;}
.anadwo-top {background:linear-gradient(90deg,#FF0055,#FF3366); padding:12px 15px; display:flex; justify-content:space-between; align-items:center; border-radius:0 0 18px 18px; margin:-20px -15px 15px -15px;}
.logo-pill {background:white; color:#FF0055; padding:5px 14px; border-radius:20px; font-weight:900; font-size:13px; letter-spacing:1px;}
.card {border-radius:20px; padding:16px; color:white; height:115px; position:relative; margin-bottom:10px; box-shadow:0 4px 12px rgba(0,0,0,0.15);}
.input-box {border:1.5px solid #FFD1DC; border-radius:18px; padding:5px; background:white;}
.bottom-nav {position:fixed; bottom:0; left:0; right:0; background:white; display:flex; justify-content:space-around; padding:12px 5px; border-top:1px solid #ffe0e6; z-index:999; border-radius:20px 20px 0 0;}
</style>
""", unsafe_allow_html=True)

# ===== TOP BAR - ANADWOAI =====
st.markdown("""
<div class="anadwo-top">
  <div style="display:flex; align-items:center; gap:8px;">
    <span style="color:white; font-size:22px;">☰</span>
    <span class="logo-pill">ANADWOAI.COM</span>
  </div>
  <div style="color:white; display:flex; gap:14px; font-size:18px;"> <span>+</span> <span>◧</span> <span>⋮</span> </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; justify-content:space-around; margin:12px 0;">
  <div style="background:#FF0055; width:46px; height:46px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:18px;">⚙</div>
  <div style="background:#FFE5EC; width:46px; height:46px; border-radius:50%; display:flex; align-items:center; justify-content:center;">💎</div>
  <div style="background:#FFF0F3; width:46px; height:46px; border-radius:50%; display:flex; align-items:center; justify-content:center;">🔊</div>
  <div style="background:#FFF0F3; width:46px; height:46px; border-radius:50%; display:flex; align-items:center; justify-content:center;">?</div>
  <div style="background:#FFE5EC; width:46px; height:46px; border-radius:50%; display:flex; align-items:center; justify-content:center;">🔔</div>
  <div style="background:#FF0055; width:46px; height:46px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white;">P</div>
</div>
<p style="text-align:center; font-weight:800; font-size:18px; margin:5px 0;">Let's get started, Philip</p>
<p style="text-align:center; color:#FF0055; font-size:12px; font-weight:600; margin-top:-5px;">🇬🇭 Powered by ANADWOAI</p>
""", unsafe_allow_html=True)

# TABS
c1,c2,c3 = st.columns(3)
with c1: st.markdown("<div style='background:#FF0055; color:white; padding:7px 10px; border-radius:20px; text-align:center; font-size:12px; font-weight:bold;'>📹 Video</div>", unsafe_allow_html=True)
with c2: st.markdown("<div style='background:white; border:1px solid #ffd1dc; padding:7px 10px; border-radius:20px; text-align:center; font-size:12px;'>🎙 Voiceover</div>", unsafe_allow_html=True)
with c3: st.markdown("<div style='background:white; border:1px solid #ffd1dc; padding:7px 10px; border-radius:20px; text-align:center; font-size:12px;'>🎨 Design</div>", unsafe_allow_html=True)

st.write("")
# INPUT
with st.container():
    idea = st.text_area("", placeholder="Enter your AnadwoAI video idea, script, or story link... e.g. Kofi goes to school...", height=130, label_visibility="collapsed")
    b1,b2,b3,b4 = st.columns(
