import streamlit as st
from streamlit_auth0_component import login_button
import jwt

# --- Auth0 Config ---
domain = st.secrets.auth0.domain
client_id = st.secrets.auth0.client_id
client_secret = st.secrets.auth0.client_secret
redirect_uri = st.secrets.auth0.redirect_uri
allowed = st.secrets.auth0.allowed_emails

# --- Auth0 Login Button ---
user_info = login_button(
    client_id=client_id,
    domain=domain,
    redirect_uri=redirect_uri,
    key="auth0",
)

# --- Access Control ---
if not user_info:
    st.warning("🔐 Please log in to access the app.")
    st.stop()

email = user_info.get("email", "")
if email not in allowed:
    st.error("🚫 You are not authorized to access this app.")
    st.stop()

# --- Your App Here ---
st.success(f"✅ Logged in as {email}")
st.title("📈 Weekly Options Stock Screener (Auth0)")
# ... insert screener code here ...
