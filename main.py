import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from itertools import cycle
from PIL import Image
import urllib.request
import base64
from db.orm import *


st.set_page_config(layout="wide",initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center; color: grey;'>Art4Shine</h1>", unsafe_allow_html=True)
# 1. as sidebar menu
with st.sidebar:
    choice = option_menu("Main Menu", ["Home",  'SignUp', 'Login',], 
        icons=['house', 'plus', 'person', 'sign'], menu_icon="cast", default_index=1)
    if choice == "Home":
        st.subheader("Home")
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password' )    
        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
			# if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)         
            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
                if task == "Add Post":
                    st.subheader("Add Your Post")
                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    st.dataframe(clean_db)
        else:
            st.warning("Incorrect Username/Password")


# image grid
col1, col2 = st.columns([5,1])
with st.container():
    with col1:
        selected = option_menu(None, ["Home", "Upload",  "Tasks", 'Settings'], 
            icons=['house', 'cloud-upload', "list-task", 'gear'], 
            menu_icon="cast", default_index=0, orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "green"},
            }
        )
        if selected == "Home":
            st.header('Art Galary')
            # st.write('This is the home page.')
            pass

        elif selected == "Upload":
            st.title("Upload")
            st.write('Upload a file.')
        elif selected == 'Tasks':
            pass
with col2:
    cart = option_menu(
                       None,["Cart"],
                            icons=['cart'],
                            menu_icon="cast", default_index=0, orientation="vertical",
                            styles={
                                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                                    "icon": {"color": "orange", "font-size": "25px"}, 
                                    "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                    "nav-link-selected": {"background-color": "green"},
                                }
                            )
    if cart == 'cart':
        ""



filteredImages = [
'https://images.unsplash.com/photo-1666533451424-90fddcfb6633?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
'https://images.unsplash.com/photo-1666555423180-729226967c76?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
'https://images.unsplash.com/photo-1506038634487-60a69ae4b7b1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=766&q=80',
'https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
'https://images.unsplash.com/photo-1549989317-6f14743af1bf?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
'https://images.unsplash.com/photo-1483921020237-2ff51e8e4b22?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
] # your images here
caption = ['Kingdom\nsize: 4x4 inch\nprice: $240', 
            'bike\nsize: 4x4 inch\nprice: $2550', 
            'switzerland\nsize: 4x4 inch\nprice: $640', 
            'paracute\nsize: 4x4 inch\nprice: $340', 
            'beach\nsize: 4x4 inch\nprice: $540', 
            'snow\nsize: 4x4 inch\nprice: $840'
            ] # your caption here
cols = cycle(st.columns(3)) 
for idx, filteredImage in enumerate(filteredImages):
    urllib.request.urlretrieve(filteredImage,str(idx)+'.jpg')
    image = Image.open( str(idx)+'.jpg')
    new_image = image.resize((400, 400),Image.LANCZOS)
    col = next(cols)
    col.image(new_image, width=320, caption=caption[idx], )
    customized_button = st.markdown("""
    <style >
    .stDownloadButton, div.stButton {text-align:center;margin-right: 50%; margin: 0 auto;}
    .stDownloadButton button, div.stButton > button:first-child {
        background-color: #ADD8E6;
        color:#000000;
        padding-left: 20px;
        padding-right: 20px;
    }
    
    .stDownloadButton button:hover, div.stButton > button:hover {
        background-color: #ADD8E6;
        color:#000000;
    }
    .fullScreenFrame > div {
    display: flex;
    justify-content: center;
    }
    """,  unsafe_allow_html=True)
    btn = col.button('add to cart ', key=idx )
        
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# add_bg_from_local('bg4.jpg') 

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