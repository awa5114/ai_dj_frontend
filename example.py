import streamlit as st
import requests

audio_file = open('ODESZA - A Moment Apart-0 - ODESZA - A Moment Apart-0.wav', 'rb')
audio_bytes = audio_file.read()
print(type(audio_bytes))
st.audio(audio_bytes, format='audio/wav')
