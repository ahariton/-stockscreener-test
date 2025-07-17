from streamlit_oauth import OAuth2Component
import streamlit as st
import requests
import jwt

# Step 1: Create the component
oauth2 = OAuth2Component(st.secrets.oauth.client_id, st.secrets.oauth.client_secret)

# Step 2: Trigger login
token = oauth2.authorize_button(
    name="Login with Auth0",
    auth_url=st.secrets.oauth.auth_url,
    token_url=st.secrets.oauth.token_url,
    redirect_uri=st.secrets.oauth.redirect_uri,
    scope="openid profile email",
    key="auth"
)

# Step 3: Fetch user info and gate access
if token:
    userinfo_response = requests.get(
        st.secrets.oauth.userinfo_endpoint,
        headers={"Authorization": f"Bearer {token['access_token']}"}
    )
    userinfo = userinfo_response.json()
    email = userinfo.get("email", "")

    if email in st.secrets.oauth.allowed_emails:
        st.success(f"✅ Logged in as {email}")
        # your app logic goes here
    else:
        st.error("🚫 You are not authorized to access this app.")
        st.stop()
else:
    st.warning("🔐 Please log in to access this app.")
    st.stop()
