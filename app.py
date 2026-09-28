import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
import requests, urllib.parse, re, os, time
from io import BytesIO
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip

st.set_page_config(page_title="AnadwoAI", page_icon="🎬", layout="centered")

st.markdown("""
<style>
header {visibility:hidden;}
.block-container {padding-top:0; padding-bottom:90px; max-width:420px;}
.anadwo-top {background:#FF0055; padding:12px; display:flex; justify-content:space-between; align-items:center; border-radius:0 0 18px 18px; margin:-20px -10px 10px -10px;}
.logo-pill {background:white; color:#FF0055; padding:5px 14px; border-radius:20px; font-weight:900; font-size:13px;}
.card {border-radius:18px; padding:14px; color:white; height:110px; margin-bottom:10px;}
.bottom-nav {position:fixed; bottom:0; left:0; right:0; background:white; display:flex; justify-content:space-around; padding:10px; border-top:1px solid #eee; z-index:999;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="anadwo-top">
  <span class="logo-pill">ANADWOAI.COM</span>
  <span style="color:white;">+ ◧ ⋮</span>
</div>
<div style="text-align:center;">
  <b>Let's get started, Philip</b><br>
  <small style="color:#FF0055;">Powered by ANADWOAI 🇬🇭</small>
</div>
""", unsafe_allow_html=True)

st.write("")
c1, c2, c3 = st.columns(3)
c1.markdown("<div style='background:#FF0055; color:white; padding:6px; border-radius:20px; text-align:center; font-size:12px;'>Video</div>", unsafe_allow_html=True)
c2.markdown("<div style='background:#f5f5f5; padding:6px; border-radius:20px; text-align:center; font-size:12px;'>Voiceover</div>", unsafe_allow_html=True)
c3.markdown("<div style='background:#f5f5f5; padding:6px; border-radius:20px; text-align:center; font-size:12px;'>Design</div>", unsafe_allow_html=True)

idea = st.text_area("Story", placeholder="Enter your AnadwoAI video idea, script, or story... e.g. Kofi goes to school everyday. He plays with his friends...", height=130, label_visibility="collapsed")

create_btn = st.button("Create with AnadwoAI ->", type="primary", use_container_width=True)

st.markdown("**AnadwoAI workflows**")
st.markdown("""
<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
  <div class="card" style="background:linear-gradient(135deg,#FF5A5F,#C70039);"><b
