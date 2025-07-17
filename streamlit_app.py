import streamlit as st

# Step 1: Kick off OIDC login if the user isn’t already signed in
if not st.user.is_logged_in:
    st.login("auth0")
    st.stop()

# Step 2: Grab the user’s email and enforce your allow-list
email = st.user["email"]
if email not in st.secrets.auth.auth0.allowed_emails:
    st.error("🚫 You are not authorized.")
    st.logout()
    st.stop()

# Step 3: At this point you know who the user is and that they’re allowed
st.success(f"✅ Logged in as {email}")

# …the rest of your app goes here…
