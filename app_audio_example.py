import streamlit as st
import requests

audio_file = open('Daniel Leseman - So Fine.mp3', 'rb')
audio_bytes = audio_file.read()
print(type(audio_bytes))
st.audio(audio_bytes, format='audio/mp3')
