import streamlit as st
from streamlit_oauth import OAuth2Component

oauth2 = OAuth2Component(
    client_id=st.secrets.oauth.client_id,
    client_secret=st.secrets.oauth.client_secret,
    authorize_url=st.secrets.oauth.auth_url,
    token_url=st.secrets.oauth.token_url,
    redirect_uri=st.secrets.oauth.redirect_uri,
)

token = oauth2.authorize_button("🔐 Log in with Auth0")

if not token:
    st.stop()

userinfo = oauth2.get_user_info(token)
email = userinfo.get("email")

if email not in st.secrets.oauth.allowed_emails:
    st.error("❌ Unauthorized")
    st.stop()

st.success(f"✅ Welcome, {email}!")
