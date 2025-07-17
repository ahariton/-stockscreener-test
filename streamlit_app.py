import streamlit as st

# Step 1: Login
user = st.login(provider="auth0")
if not user:
    st.stop()

# Step 2: Access control
email = user.get("email", "")
allowed = st.secrets.oauth.auth0.allowed_emails

if email not in allowed:
    st.error("🚫 You are not authorized to access this app.")
    st.logout()
    st.stop()

# Step 3: Proceed with app
st.success(f"✅ Logged in as {email}")
# ... your app code ...
