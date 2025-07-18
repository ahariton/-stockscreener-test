
import datetime as dt
import re
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from tqdm import tqdm

def normalize_symbol(sym: str) -> str:
    return sym.replace('.', '-').strip().upper()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

WEEKLY_URL = "https://www.cboe.com/us/options/symboldir/weeklys_options/"
CSV_URL = "https://www.cboe.com/available_weeklys/get_csv_download/"
TICKER_RE = re.compile(r"^[A-Z]{1,5}(?:\.[A-Z])?$")

def load_z_map() -> Dict[str, float]:
    url = "https://stockanalysis.com/api/screener/s/d/zScore"
    rows = requests.get(url, headers=HEADERS, timeout=15).json()["data"]["data"]
    z_map = {}
    for sym, val in rows:
        try:
            z_map[str(sym).upper()] = float(val)
        except (TypeError, ValueError):
            z_map[str(sym).upper()] = np.nan
    return z_map

def _parse_weeklys_html() -> pd.DataFrame:
    html = requests.get(WEEKLY_URL, headers=HEADERS, timeout=20).text
    soup = BeautifulSoup(html, "html.parser")
    tokens = list(soup.stripped_strings)
    pairs: list[Tuple[str, str]] = []
    for i, token in enumerate(tokens):
        if TICKER_RE.match(token) and i:
            name = tokens[i - 1]
            if name.lower().startswith(("symbol", "ticker", "name of underlying")):
                continue
            pairs.append((token, name))
    return pd.DataFrame(pairs, columns=["Symbol", "Company"]).drop_duplicates()

def _parse_weeklys_csv() -> pd.DataFrame:
    csv = requests.get(CSV_URL, headers=HEADERS, timeout=20).content.decode()
    rows = []
    for line in csv.splitlines():
        parts = [p.strip('"') for p in line.split(",")]
        if parts and TICKER_RE.match(parts[0]):
            rows.append((parts[0], parts[1] if len(parts) > 1 else ""))
    return pd.DataFrame(rows, columns=["Symbol", "Company"]).drop_duplicates()

def get_weekly_universe(excluded_symbols) -> pd.DataFrame:
    try:
        df = _parse_weeklys_html()
        if df.empty:
            raise ValueError
    except Exception:
        df = _parse_weeklys_csv()
    df["Symbol"] = df["Symbol"].apply(normalize_symbol)
    df = df[~df["Symbol"].isin(excluded_symbols)].reset_index(drop=True)
    return df[["Symbol", "Company"]]

def price_stats(tkr: yf.Ticker) -> Tuple[float, float]:
    try:
        hist = tkr.history(period="1y")
        if hist.empty:
            return np.nan, np.nan
        last = hist["Close"].iloc[-1]
        high = hist["Close"].max()
        return (high - last) / high, last
    except Exception:
        return np.nan, np.nan

def iv14(tkr: yf.Ticker, target_dte: int = 14, window_dte: int = 4) -> float:
    """
    Compute the 14-day implied volatility using Yahoo's impliedVolatility,
    cleaning up NaNs, zeros, and capping to handle Yahoo's occasional extreme data.
    Returns median of 6 strikes nearest ATM.
    """
    today = dt.date.today()

    # 1) Find expiries with positive DTE
    exps = []
    for exp_str in tkr.options:
        try:
            dte = (dt.datetime.strptime(exp_str, "%Y-%m-%d").date() - today).days
            if dte > 0:
                exps.append((exp_str, dte))
        except ValueError:
            continue
    if not exps:
        return np.nan

    # 2) Pick the expiry nearest to target_dte
    window = [e for e in exps if abs(e[1] - target_dte) <= window_dte]
    chosen = min(window or exps, key=lambda x: abs(x[1] - target_dte))[0]

    # 3) Fetch option chain and compute distance from spot
    chain = tkr.option_chain(chosen)
    df = pd.concat([chain.calls, chain.puts], ignore_index=True)
    spot = tkr.history(period="1d")["Close"].iloc[-1]
    df["dist"] = (df["strike"] - spot).abs()

    # 4) Take the 6 nearest strikes
    nearest = df.nsmallest(6, "dist")

    # 5) Clean implied vols: drop NaNs, zero or >100% cap
    ivs = nearest["impliedVolatility"].dropna()
    ivs = ivs[(ivs > 0.01) & (ivs <= 1.0)]

    # 6) Return median if any left, else NaN
    return float(ivs.median()) if not ivs.empty else np.nan

def next_earnings(tkr: yf.Ticker) -> dt.date | None:
    today = dt.date.today()
    try:
        calendar = tkr.calendar
        earnings_dates = calendar.get("Earnings Date", [])

        # Pick first strictly future earnings date
        return next((d for d in earnings_dates if d > today), None)


    except Exception as e:

        return None

def passes_eps_filter(tkr: yf.Ticker, eps_years: int, required: int) -> bool:
    try:
        stmt = tkr.income_stmt
        if stmt.empty:
            return False
        for key in ("Diluted EPS", "Basic EPS", "Basic & Diluted EPS", "EPS"):
            if key in stmt.index:
                row = stmt.loc[key].astype(float)
                break
        else:
            return False
        return (row.iloc[:eps_years] > 0).sum() >= required
    except Exception:
        return False




def run_screener(
    excluded_symbols: list[str],
    min_price: float,
    max_price: float,
    eps_years: int,
    eps_positive_required: int,
    pct_off_high: float,
    z_min: float = 0.0,
    show_progress: bool = False
) -> pd.DataFrame:
    excluded_symbols = [normalize_symbol(s) for s in excluded_symbols]
    universe = get_weekly_universe(excluded_symbols)
    z_map = load_z_map()
    z_ok = {sym for sym, z in z_map.items() if (np.isnan(z) or z >= z_min)}
    tickers = [sym for sym in universe["Symbol"] if (sym not in z_map) or (sym in z_ok)]
    names = dict(zip(universe["Symbol"], universe["Company"]))

    rows: List[Dict] = []

    progress_bar = None
    status = None
    if show_progress:
        import streamlit as st
        st.write(f"Screening {len(tickers)} tickers (Z > 3 or missing)…")
        progress_bar = st.progress(0)
        status = st.empty()

    for i, sym in enumerate(tickers):
        if show_progress and progress_bar:
            progress_bar.progress((i + 1) / len(tickers))
            status.text(f"Screening {i+1}/{len(tickers)} — {sym}")

        tkr = yf.Ticker(sym)
        if not passes_eps_filter(tkr, eps_years, eps_positive_required):
            continue
        pct_off, price = price_stats(tkr)
        if (
            np.isnan(pct_off) or np.isnan(price)
            or not (min_price <= price <= max_price and pct_off >= pct_off_high)
        ):
            continue
        iv = iv14(tkr)
        z = z_map.get(sym, np.nan)
        try:
            info = tkr.info
            sector = info.get("sector", "")
            industry = info.get("industry", "")
        except Exception:
            sector, industry = "", ""
        earn_date = next_earnings(tkr)
        earnings_cell = earn_date.isoformat() if earn_date else ""
        if earn_date and (earn_date - dt.date.today()).days <= 7:
            earnings_cell += "  WARNING - earnings within the next 7 days"
        rows.append({
            "Symbol": sym,
            "Company": names.get(sym, ""),
            "Sector": sector,
            "Industry": industry,
            "Price": round(price, 2),
            "% Off High": round(pct_off * 100, 1),
            "IV": round(iv * 100, 1) if not np.isnan(iv) else np.nan,
            "Z": round(z, 2) if not np.isnan(z) else np.nan,
            "Earnings": earnings_cell,
        })

    return pd.DataFrame(rows).sort_values("IV", ascending=False)
