mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"alex10estadistica@gmail.com\"\n\
" > ~/.streamlit/credentials.toml



[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml