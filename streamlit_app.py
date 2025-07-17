import streamlit as st

# DEBUG: show first/last 4 chars of your loaded secret
secret = st.secrets["auth"]["auth0"]["client_secret"]
prefix, suffix = secret[:4], secret[-4:]
st.write("🔑 client_secret starts with:", prefix)
st.write("🔑 client_secret ends   with:", suffix)
st.stop()


# # Kick off login if necessary
# if not st.user.is_logged_in:
#     st.login("auth0")
#     st.stop()

# email = st.user["email"]
# if email not in st.secrets.auth.auth0.allowed_emails:
#     st.error("🚫 You are not authorized.")
#     st.logout()
#     st.stop()

# st.success(f"✅ Logged in as {email}")
# # …rest of your app…
