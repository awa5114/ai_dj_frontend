from os import write
import streamlit as st
import numpy as np
import pandas as pd
import params
import gcp_storage

#Don't forget to change the name.
file = '64_kygo_combined2.wav'
gcp_storage.get_mixed_audio(file)
mix = f'{params.TEMP_MIXED_FOLDER}/{file}'

_, col2, _ = st.beta_columns([1, 2, 1])

with col2:
    st.title("DJ for dummies")
#st.markdown("""# DJ for dummies""")
  
st.markdown("""## Paste the Youtube link of your song below""")
yt_link = st.text_input('', '' )

if st.button('Create'):
    print('button clicked!')
    st.write('Creating your unique song 🎉')
    file = '64_kygo_combined2.wav'
    gcp_storage.get_mixed_audio(file)
    mix = f'{params.TEMP_MIXED_FOLDER}/{file}'
    st.balloons()
else:
    st.write('Nothing created so far 😞')

st.audio(mix, format='audio/wav', start_time=0)

audio_file = open(mix, 'rb')
audio_bytes = audio_file.read()
#st.audio(audio_bytes, format='audio/wav')
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
    
def get_slider_data():
    print('get_slider_data called')
    return pd.DataFrame({
    'first column': list(range(1, 11)),
    'second column': np.arange(10, 101, 10)
        })

df = get_slider_data()

option = st.slider('Select a modulus', 1, 10, 3)

filtered_df = df[df['first column'] % option == 0]

st.write(filtered_df)