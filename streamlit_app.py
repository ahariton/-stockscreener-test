import streamlit as st

# ─── DEBUG BLOCK ──────────────────────────────────────────────────────────

st.write("Client ID:", st.secrets.auth.auth0.client_id)
st.write("Client Secret:", st.secrets.auth.auth0.client_secret)
st.stop()

# # ▶️ DEBUG: print out what redirect_uri we actually loaded
# redirect = st.secrets["auth"]["redirect_uri"]
# st.write("🔍 Loaded redirect_uri:", redirect)
# st.stop()


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
