from os import write
import streamlit as st
import requests
import numpy as np

url = "https://ai-dj-container-btoorogyaa-ez.a.run.app"

_, col2, _ = st.beta_columns([1, 2, 1])

with col2:
    st.title("DJ for dummies")

st.markdown("""## Song filename """)
song_name = st.text_input('song filename', '' )
#1019315 Guido Sava - Fever (Original Mix).wav

params = {
    'filename': song_name, 
}

if st.button('Create'):
    print('button clicked!')
    st.write('Creating ydour unique song 🎉')
    response = requests.get(url, params=params, stream=True)
    bts = response.raw.read()
    st.audio(bts)
else:
    st.write('Nothing created so far 😞')


st.write("###")

st.markdown("""### Enjoy the newly created song by ai_dj and tell us what you think about it!""")

if st.button('I love it!'):
    st.write('Fantastic' '🎉 ' 'will keep producing the good stuff' " Thank you, come again.")
    st.balloons()
st.write("#")

if st.button("Mhhh, it's ok"):  
    st.write("Nice, we'll make it even better! 🎉" " Thank you, come again.")
st.write("#")
 
if st.button('Yuk, I hate it...'):
    print('button clicked!')
    st.write('Thanks for your feedback, the next one will be better.')
else:
    st.write("You didn't tell us your thoughts yet 😞")