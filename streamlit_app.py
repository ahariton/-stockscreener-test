import streamlit as st
import requests

from streamlit_oauth import OAuth2Component

oauth2 = OAuth2Component(
    client_id=st.secrets.oauth.client_id,
    client_secret=st.secrets.oauth.client_secret,
    redirect_uri=st.secrets.oauth.redirect_uri,
    authorize_endpoint=st.secrets.oauth.auth_url,
    token_endpoint=st.secrets.oauth.token_url,
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
