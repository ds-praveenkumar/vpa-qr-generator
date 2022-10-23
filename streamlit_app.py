import streamlit as st
from PIL import Image
import requests
import json
import base64
import time
from decimal import *


name = "Art4Shine"
vpa= "praveenkr2208@okhdfcbank"

img = Image.open('icon.jpeg')
st.set_page_config( page_title="Art4Shine.com", page_icon=img) 

def generate_qr(amount):

    url = "https://upiqr.in/api/qr"

    payload = json.dumps({
    "name": name,
    "vpa": vpa,
    "format": "png",
    "amount": amount
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, stream=True)
    return response.content.decode()


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    _left, mid, _right = st.columns(3)
    
    with mid:
        st.subheader('Art4Shine')
        st.write(html, unsafe_allow_html=True)
        st.info(f'UPI ID: {vpa}', icon="ℹ️") 

with st.form(key='payment'):
    # st.header( 'Art4Shine Payment link ')
    st.markdown(f'<h1 style="color:#33ffd7;font-size:24px;">{"Art4Shine Payment link "}</h1>', unsafe_allow_html=True)
    customer_name = st.text_input("Customer Name")
    amount = st.text_input("Amount")

    if st.form_submit_button("submit"):
        amount = '{0:.2f}'.format(float(amount))
        if (float(amount) > 0.0)  : 
            img_data = generate_qr(amount)
            render_svg(img_data)
            st.balloons()
            print('QR Code generated')
        else:
            st.exception("Enter valid amount like 20.00 in INR")

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
footer_note = """

	Copyright Art4Shine.com © 2022

"""
st.markdown( footer_note, unsafe_allow_html=False)
            
    