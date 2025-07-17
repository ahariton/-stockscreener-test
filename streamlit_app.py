import streamlit as st
import requests

from streamlit_oauth import OAuth2Component

oauth2 = OAuth2Component(st.secrets.oauth.client_id, st.secrets.oauth.client_secret)

token = oauth2.authorize_button(
    name="Login with Auth0",
    authorize_url=st.secrets.oauth.auth_url,
    token_url=st.secrets.oauth.token_url,
    redirect_uri=st.secrets.oauth.redirect_uri,
    key="auth",
)

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
