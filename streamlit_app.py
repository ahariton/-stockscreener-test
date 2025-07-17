import streamlit as st

#─── DEBUG BLOCK ──────────────────────────────────────────────────────────

# Kick off login if necessary
if not st.user.is_logged_in:
    st.login("auth0")
    st.stop()

email = st.user["email"]
if email not in st.secrets.auth.auth0.allowed_emails:
    st.error("🚫 You are not authorized.")
    st.logout()
    st.stop()

st.success(f"✅ Logged in as {email}")
# …rest of your app…
