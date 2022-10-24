mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml

echo "\
[theme]\n\
primaryColor=\"#2214c7\"\n\
backgroundColor=\"#F0FFF0\"\n\
secondaryBackgroundColor=\"#e8eef9\"\n\
textColor=\"#000000\"\n\
\n\
" >> ~/.streamlit/config.toml