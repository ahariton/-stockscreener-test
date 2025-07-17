import streamlit as st
from streamlit_oauth import OAuth2Component

# Setup Auth0 with values from secrets.toml
oauth2 = OAuth2Component(
    client_id=st.secrets.oauth.client_id,
    client_secret=st.secrets.oauth.client_secret,
    auth_url=st.secrets.oauth.auth_url,
    token_url=st.secrets.oauth.token_url,
    redirect_uri=st.secrets.oauth.redirect_uri,
    user_info_url=st.secrets.oauth.userinfo_endpoint,
)

# Authenticate user
token = oauth2.get_token()

# If user not authenticated, stop the app
if token is None:
    st.stop()

# Get user info
user_info = oauth2.get_user_info(token)
email = user_info.get("email", "")

# Restrict access
if email not in st.secrets.oauth.allowed_emails:
    st.error("🚫 Access denied")
    st.stop()

# App content for authorized users
st.success(f"✅ Logged in as: {email}")
st.title("📈 Test: Weekly Options Screener with Auth0")
st.write("Welcome to the test version of your secure app!")
