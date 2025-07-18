import streamlit as st

# 1) If not logged in, send to Auth0
if not st.user.is_logged_in:
    st.login("auth0")
    st.stop()

# 2) Grab their email
email = st.user["email"]

# 3) If it’s not in your allow-list, show a message and stop the app
if email not in st.secrets.auth.auth0.allowed_emails:
    st.error("🚫 You are not authorized to use this app.")
    st.stop()

# 4) Otherwise they’re good
st.success(f"✅ Logged in as {email}")
# …rest of your app…


# import streamlit as st

# # ─── DEBUG: Initial state ─────────────────────────────────────────────
# st.write("🔍 [DEBUG] user.is_logged_in:", st.user.is_logged_in)

# # Print the secrets we care about
# st.write("🔍 [DEBUG] redirect_uri:", st.secrets["auth"]["redirect_uri"])
# st.write("🔍 [DEBUG] metadata_url:", st.secrets["auth"]["auth0"]["server_metadata_url"])
# st.write("🔍 [DEBUG] client_id:", st.secrets["auth"]["auth0"]["client_id"])
# # (don't print the full client_secret!)
# st.write(
#     "🔍 [DEBUG] client_secret matches prefix/suffix:",
#     st.secrets["auth"]["auth0"]["client_secret"][:4],
#     "...",
#     st.secrets["auth"]["auth0"]["client_secret"][-4:],
# )

# # ─── DEBUG: About to call st.login ────────────────────────────────────
# if not st.user.is_logged_in:
#     st.write("▶️ [DEBUG] calling st.login('auth0') now")
#     st.login("auth0")
#     st.write("❌ [DEBUG] this line should never render (we should have been redirected)")
#     st.stop()

# # ─── DEBUG: After login ───────────────────────────────────────────────
# st.write("✅ [DEBUG] returned from st.login, user.is_logged_in:", st.user.is_logged_in)

# # Fetch email and debug it
# email = st.user.get("email", None)
# st.write("🔍 [DEBUG] st.user['email']:", email)

# # Authorization check
# if email not in st.secrets.auth.auth0.allowed_emails:
#     st.write("🚫 [DEBUG] email not in allowed_emails list")
#     st.error("🚫 You are not authorized.")
#     st.logout()
#     st.stop()

# st.write("✅ [DEBUG] email is allowed, proceeding to app")
# st.success(f"✅ Logged in as {email}")

# # …rest of your app…
# st.write("🎉 [DEBUG] reached end of script")
