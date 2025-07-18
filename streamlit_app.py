import streamlit as st
import pandas as pd
from screener_utils import run_screener

# 1) If not logged in, send to Auth0
if not st.user.is_logged_in:
    st.login("auth0")
    st.stop()

# 2) Grab their email
email = st.user["email"]

# 3) If it’s not in your allow-list, show a message and stop the app
if email not in st.secrets.auth.auth0.allowed_emails:
    st.error(
        "🚫 You are not authorized to use this app.\n\n"
        "If you accidentally signed in with the wrong email, click the button below to try again."
    )
    if st.button("🔄 Sign in with a different account"):
        # clear out the current session and kick off login again
        st.logout()
        st.experimental_rerun()
    st.stop()

# 4) Otherwise they’re good
st.success(f"✅ Logged in as {email}")
def normalize_symbol(sym: str) -> str:
    return sym.replace('.', '-').strip().upper()

st.cache_data.clear()

st.title("📈 Weekly Options Stock Screener")

st.markdown("""
### 🧠 About This Screener

This tool evaluates all currently listed companies offering weekly options.

It applies several filters to highlight potentially strong option candidates:

- 📉 Bankruptcy risk is screened out using a quantitative Altman-Z filter  
- 💸 Companies must be trading at least 25% below their 52-week high (customizable)  
- 📊 Defaults to excluding companies without positive earnings in at least 3 of the last 4 years (customizable)  
- 🔍 Final results are sorted by estimated 14-day implied volatility.  

⚠️ Heads up: IV data may be inaccurate outside of market hours — for best results, check during regular trading sessions.

You can customize the:
- Bankruptcy Risk
- Price range (helpful to match your account size or option premium targets)
- % off 52-week high threshold
- Earnings filters

This information is provided for the personal use of the individual who generated it using the Stock Screener App. Redistribution, sharing, or commercial use of this file, 
in whole or in part, is strictly prohibited.

Once you click **Run Screener**, qualifying companies will appear below, sorted by IV.              
""")


# Static default excluded list (never modified)
DEFAULT_EXCLUDED = [normalize_symbol(s) for s in [
    "VIX", "CBTX", "MBTX", "MXACW", "MXEA", "MXEF", "MXUSA", "MXWLD",
    "MRUT", "XSP", "NANOS", "RUT", "OEX", "XEO", "SPX", "ETHU", "MSTX", "BOIL", "UVIX",
    "TSLL", "KOLD", "SOXS", "NVDL", "LABU", "SOXL", "YANG", "YINN", "UVXY", "DPST",
    "TZA", "SQQQ", "TNA", "TQQQ", "UCO", "SVIX", "SPXU", "CHAU", "TMF", "ARKG", "TAN",
    "SVXY", "ITB", "ZI", "CSIQ", "SEDG", "VFC", "DQ", "RH", "ABR", "HE", "ARM", "PDD",
    "JD", "BIDU", "GLXY"
]]



# Initialize temporary added symbols
if "temp_excluded" not in st.session_state:
    st.session_state.temp_excluded = []

# Input to add temporary symbol
new_symbol = None
if new_symbol and not st.session_state.get("reran_once", False):
    symbol = normalize_symbol(new_symbol)
    if symbol and symbol not in st.session_state.temp_excluded and symbol not in DEFAULT_EXCLUDED:
        st.session_state.temp_excluded.append(symbol)
        st.session_state.reran_once = True
        st.rerun()

# reset after rerun
if "reran_once" in st.session_state:
    del st.session_state.reran_once

# Optionally show the combined exclusion list
with st.expander("🔍 View current (temporary + default) excluded symbols", expanded=False):
    combined_list = DEFAULT_EXCLUDED + st.session_state.temp_excluded
    st.write(", ".join(combined_list))
    if st.button("Clear temporary exclusions"):
        st.session_state.temp_excluded = []
        st.rerun()


# Screener parameters
z_score_threshold = st.select_slider(
    "Minimum Altman Z-Score (financial stability)",
    options=[0.0, 1.8, 3.0],
    value=3.0,
    format_func=lambda x: f">{x} ({'All' if x == 0.0 else 'Some Risk' if x == 1.8 else 'Low Risk'})"
)
min_price = st.number_input("Min Price", min_value=5, max_value=500, value=10, step=5)
max_price = st.number_input("Max Price", min_value=10, max_value=1000, value=300, step=5)
eps_years = st.number_input("Years to check EPS", min_value=4, max_value=4, value=4)
eps_required = st.number_input("Min years EPS positive", min_value=0, max_value=10, value=3)
pct_off_high = st.slider("% Off High Threshold", min_value=0.0, max_value=1.0, value=0.25, step=.05)

@st.cache_data(show_spinner=False)
def run_screener_cached(*args, **kwargs):
    return run_screener(*args, **kwargs)



# Run the screener
if st.button("Run Screener"):
    with st.spinner("Running..."):
        try:
            full_excluded = DEFAULT_EXCLUDED + st.session_state.temp_excluded
            df = run_screener_cached(
                full_excluded,
                min_price,
                max_price,
                int(eps_years),
                int(eps_required),
                float(pct_off_high),
                z_min=z_score_threshold,
                show_progress=True
            )
            st.success(f"✅ Found {len(df)} stocks")
            st.dataframe(df, hide_index=True)

            st.markdown(
                """
                <div style="font-size: 0.9em; color: gray;">
                    <strong>Disclaimer:</strong> This data is provided for your personal use only.
                    Redistribution, sharing, or commercial use of this information, in whole or in part, is strictly prohibited.
                </div>
                """,
                unsafe_allow_html=True
            )

            # Add disclaimer to CSV
            # disclaimer = "# Disclaimer: This file is provided for the personal use of the individual who generated it using the Stock Screener App. Redistribution, sharing, or commercial use of this file, in whole or in part, is strictly prohibited.\n"
            # csv_buffer = StringIO()
            # csv_buffer.write(disclaimer)
            # df.to_csv(csv_buffer, index=False)
            # csv_data = csv_buffer.getvalue()

            # Download button without disclaimer
            csv_data = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name="screen_results.csv",
                mime="text/csv"
)
        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("[andy@challeninvestments.com](mailto:andy@challeninvestments.com)")

with st.expander("📄 Legal & Subscription Terms", expanded=False):
    st.markdown("""
    - 📄 [Terms of Service & Privacy Policy](https://github.com/ahariton/stockscreener/blob/main/terms/Terms_of_Service_and_Privacy_Policy.docx?raw=true)  
    - 🛒 [Checkout Terms & Conditions](https://github.com/ahariton/stockscreener/blob/main/terms/Stripe_Checkout_Terms_and_Conditions.docx?raw=true)  
    - 📃 [Subscription Agreement](https://github.com/ahariton/stockscreener/blob/main/terms/Stock_Screener_Subscription_Agreement_with_Downtime.docx?raw=true)
    """)
