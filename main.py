import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from itertools import cycle
from PIL import Image
import urllib.request
import base64
from db.orm import *
from streamlit_elements import elements, mui, html, sync, dashboard
import extra_streamlit_components as stx

img = Image.open('icon.jpeg')
st.set_page_config(layout="wide",initial_sidebar_state="collapsed", page_icon=img)

st.markdown("<h1 style='text-align: center; color: purple;'>Art4Shine</h1>", unsafe_allow_html=True)
# 1. as sidebar menu
with st.sidebar:
    choice = option_menu("Main Menu", ["Home",  'SignUp', 'Login', 'About Us'], 
        icons=['house', 'plus', 'person', 'info'], menu_icon="cast", default_index=1)
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
    elif choice == 'About Us':
        with open( 'about.html') as f:
            about = f.read()
        components.html(about, height=600)

# image crousel
IMAGES = [
    "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920",
    "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
    "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920",
    "https://unsplash.com/photos/S5uIITJDq8Y/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjUyOTAzMzAz&force=true&w=1920",
    "https://unsplash.com/photos/E4bmf8BtIBE/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjUyOTEzMzAw&force=true&w=1920",
]

def slideshow_swipeable(images):
    # Generate a session state key based on images.
    key = f"slideshow_swipeable_{str(images).encode().hex()}"

    # Initialize the default slideshow index.
    if key not in st.session_state:
        st.session_state[key] = 0

    # Get the current slideshow index.
    index = st.session_state[key]

    # Create a new elements frame.
    with elements(f"frame_{key}"):

        # Use mui.Stack to vertically display the slideshow and the pagination centered.
        # https://mui.com/material-ui/react-stack/#usage
        with mui.Stack(spacing=2, alignItems="center"):

            # Create a swipeable view that updates st.session_state[key] thanks to sync().
            # It also sets the index so that changing the pagination (see below) will also
            # update the swipeable view.
            # https://mui.com/material-ui/react-tabs/#full-width
            # https://react-swipeable-views.com/demos/demos/
            with mui.SwipeableViews(index=index, resistance=True, onChangeIndex=sync(key)):
                for image in images:
                    html.img(src=image, css={"width": "100%"})

            # Create a handler for mui.Pagination.
            # https://mui.com/material-ui/react-pagination/#controlled-pagination
            def handle_change(event, value):
                # Pagination starts at 1, but our index starts at 0, explaining the '-1'.
                st.session_state[key] = value-1

            # Display the pagination.
            # As the index value can also be updated by the swipeable view, we explicitely
            # set the page value to index+1 (page value starts at 1).
            # https://mui.com/material-ui/react-pagination/#controlled-pagination
            mui.Pagination(page=index+1, count=len(images), color="primary", onChange=handle_change)


def slideshow_transition(images, transition):
    # Generate a session state key based on images.
    key = f"slideshow_transition_{str(images).encode().hex()}"

    # Initialize the default slideshow page.
    if key not in st.session_state:
        st.session_state[key] = 1

    # Get the current slideshow index.
    page = st.session_state[key]

    # Create a new elements frame.
    with elements(f"frame_{key}"):

        # Use mui.Stack to vertically display the slideshow and the pagination centered.
        # https://mui.com/material-ui/react-stack/#usage
        with mui.Stack(spacing=2, alignItems="center"):

            # Create a CSS grid.
            # All slides will be displayed in the same column and row, they will overlap.
            # https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout
            with html.div(css={"display": "grid", "gridTemplateColumns": "1fr", "overflow": "hidden"}):

                # Iterate over images.
                # Generate an index/page that starts at 1 to check which image is selected.
                for page, image in enumerate(images, 1):
                    selected = (st.session_state[key] == page)

                    # Wrap the image in a transition.
                    # mui.Grow and mui.Fade takes a 'in' property, however 'in' is also
                    # a python keyword you cannot use as argument name. To bypass this
                    # issue, you can just append an underscore.
                    # https://mui.com/material-ui/transitions/
                    with mui[transition](in_=selected):
                        # Display the image in the first column and row.
                        html.img(src=image, css={
                            "gridRow": 1,
                            "gridColumn": 1,
                            "width": "100%",
                        })

            # Display the pagination.
            # Synchronize onChange callback's second parameter with st.session_state[key].
            # Ignore the first parameter by using None as first argument in sync().
            # https://mui.com/material-ui/react-pagination/#controlled-pagination
            # https://mui.com/material-ui/api/pagination/#props (onChange)
            mui.Pagination(count=len(images), color="primary", onChange=sync(None, key))

# image grid
col1, col2 = st.columns([5,1])
with st.container():
    slideshow_swipeable(IMAGES)
    with col1:
        selected = option_menu(None, ["Home", "About", 'Shop'], 
            icons=['house', 'snow', 'shop'], 
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
        elif selected == 'About':
            with open( 'about.html') as f:
                about = f.read()
                components.html(about, height=600)
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
components.iframe('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d4945540.621597939!2d-6.812747151421461!3d52.75357715039033!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47d0a98a6c1ed5df%3A0xf4e19525332d8ea8!2sEngland%2C%20UK!5e0!3m2!1sen!2sin!4v1666694062398!5m2!1sen!2sin" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade')

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