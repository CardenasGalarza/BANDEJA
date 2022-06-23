mkdir -p ~/.streamlit/
echo "[general]  
email = \"m.fuad.rafi@gmail.com\""  > ~/.streamlit/config.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false"  >> ~/.streamlit/config.toml