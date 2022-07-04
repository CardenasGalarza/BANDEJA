mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"alex10estadistica@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[theme]\n\
base='light'\n\
primaryColor='#f63366'\n\
backgroundColor='#355c7d'\n\
secondaryBackgroundColor = '#d6d5d5'\n\
textColor='#000000'\n\
font = 'sans serif'\n\

[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml