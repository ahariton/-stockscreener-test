import streamlit as st

# ─── DEBUG BLOCK ──────────────────────────────────────────────────────────
# Don’t call st.login yet—just dump the values we care about and stop.
redirect = st.secrets["auth"]["redirect_uri"]
metadata = st.secrets["auth"]["auth0"]["server_metadata_url"]
client_id = st.secrets["auth"]["auth0"]["client_id"]
st.write("🔍 redirect_uri loaded:", redirect)
st.write("🔍 server_metadata_url:", metadata)
st.write("🔍 client_id:", client_id)
st.stop()
# ────────────────────────────────────────────────────────────────────────────

# (Your real login logic would go below here)
# if not st.user.is_logged_in:
#     st.login("auth0")
#     st.stop()

# # ▶️ DEBUG: show exactly what Streamlit read from secrets
# st.write("🔑 redirect_uri:", st.secrets["auth"]["redirect_uri"])
# st.write("🎫 client_id:   ", st.secrets["auth"]["auth0"]["client_id"])
# st.write("🔒 client_secret:", st.secrets["auth"]["auth0"]["client_secret"])
# st.stop()

# import streamlit as st
# st.write("Client ID:", st.secrets.auth.auth0.client_id)
# st.write("Client Secret:", st.secrets.auth.auth0.client_secret)
# st.stop()

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
