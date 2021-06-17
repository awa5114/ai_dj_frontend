import streamlit as st
import requests

'''
# TaxiFareModel app
'''

st.markdown('''
This app takes ride parameters and predicts the fare price based on a machine learning model
''')

'''
## Ride parameters
'''
date_and_time = st.text_input("Date and Time", "2012-10-06 12:10:20")
pickup_long = st.text_input("Pickup Longitude", 40.7614327)
pickup_lat = st.text_input("Pickup Latitude", -73.9798156)
dropoff_long = st.text_input("Dropoff Longitude", 40.6513111)
dropoff_lat = st.text_input("Dropoff Latitude", -73.8803331)
passenger_count = st.text_input("Passenger Count", 2)

'''
## Make prediction
'''

url = 'https://taxifare.lewagon.ai/predict'

params = {
    "pickup_datetime": date_and_time,
    "pickup_longitude": pickup_long,
    "pickup_latitude": pickup_lat,
    "dropoff_longitude": dropoff_long,
    "dropoff_latitude": dropoff_lat,
    "passenger_count": passenger_count 
}

if st.button('Make Prediction'):
    r = requests.get(url, params=params)
    json = r.json()
    st.write('result: {}'.format(json['prediction']))
