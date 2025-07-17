import streamlit as st
from streamlit_oauth import OAuth2Component
import requests

oauth2 = OAuth2Component(
    client_id=st.secrets.oauth.client_id,
    client_secret=st.secrets.oauth.client_secret,
    auth_url=st.secrets.oauth.auth_url,
    token_url=st.secrets.oauth.token_url,
    redirect_uri=st.secrets.oauth.redirect_uri,
)

token = oauth2.authorize_button("🔐 Login with Auth0", "auth0_login")

if token:
    resp = requests.get(
        st.secrets.oauth.userinfo_endpoint,
        headers={"Authorization": f"Bearer {token['access_token']}"}
    )
    user_info = resp.json()
    email = user_info.get("email", "")

    if email not in st.secrets.oauth.allowed_emails:
        st.error("🚫 Unauthorized user")
        st.stop()

    st.success(f"✅ Logged in as {email}")
else:
    st.stop()
