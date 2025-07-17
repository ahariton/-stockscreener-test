import streamlit as st

# DEBUG BLOCK
redirect = st.secrets["auth"]["redirect_uri"]
metadata = st.secrets["auth"]["auth0"]["server_metadata_url"]
client_id = st.secrets["auth"]["auth0"]["client_id"]

st.write("🔍 redirect_uri loaded:", redirect)
st.write("🔍 server_metadata_url:", metadata)
st.write("🔍 client_id:", client_id)
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
