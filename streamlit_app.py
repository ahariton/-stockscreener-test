import streamlit as st

# Simple login using Streamlit's native login
user = st.login()

if not user:
    st.stop()

# Restrict access by email
ALLOWED_USERS = ["andrewhariton@gmail.com", "teammate@company.com"]
if user.email not in ALLOWED_USERS:
    st.error("🚫 Unauthorized access.")
    st.stop()

st.title("📈 Weekly Options Stock Screener")
# ... your app here ...
