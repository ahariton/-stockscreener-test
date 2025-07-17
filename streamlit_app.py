import streamlit as st

# Login with Auth0
user = st.login(provider="auth0")

# Stop if not logged in
if not user:
    st.stop()

# Authorization check
email = user.get("email", "")
if email not in st.secrets["auth"]["auth0"]["allowed_emails"]:
    st.error("🚫 Unauthorized user.")
    st.logout()
    st.stop()

st.success(f"✅ Logged in as {email}")
