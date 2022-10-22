import streamlit as st
from PIL import Image
import requests
import json
import base64
import time
from decimal import *
st.set_page_config()

name = "Art4Shine"
vpa= "praveenkr2208@okhdfcbank"

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
            
    