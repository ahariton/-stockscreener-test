import streamlit as st
from streamlit_oauth import OAuth2Component
import requests

CLIENT_ID = st.secrets.oauth.client_id
CLIENT_SECRET = st.secrets.oauth.client_secret
REDIRECT_URI = st.secrets.oauth.redirect_uri
SCOPE = "openid profile email"

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET)

if 'token' not in st.session_state:
    result = oauth2.authorize_button("🔐 Login with Auth0", REDIRECT_URI, SCOPE)
    if result and 'token' in result:
        st.session_state.token = result['token']
        st.rerun()
    else:
        st.stop()

token = st.session_state['token']
user_info = requests.get(
    st.secrets.oauth.userinfo_endpoint,
    headers={"Authorization": f"Bearer {token['access_token']}"}
).json()

email = user_info.get("email", "")
if email not in st.secrets.oauth.allowed_emails:
    st.error("🚫 Unauthorized")
    st.stop()

st.success(f"✅ Logged in as {email}")
# ... your screener logic here ...
