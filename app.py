import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils.rates import get_cached_rates
import MetaTrader5 as mt
from datetime import datetime
import pandas as pd
from utils.indicators import vwap, ema
from utils.checker import bars_since_cross
from utils.styling import highlight_cross
from utils.login import init_login

# --- Autorefresh every 60s ---
st_autorefresh(interval=15 * 1000, key="data_refresh")

# --- Login to MetaTrader 5 ---
if not init_login():
    st.warning("Please connect to MetaTrader 5 to proceed.")
    st.stop()

# --- Constants ---
timeframes = {
    "M1": mt.TIMEFRAME_M1,
    "M5": mt.TIMEFRAME_M5,
    "M15": mt.TIMEFRAME_M15,
    "M30": mt.TIMEFRAME_M30,
    "H1": mt.TIMEFRAME_H1,
    "H4": mt.TIMEFRAME_H4,
    "D1": mt.TIMEFRAME_D1,
}

fx_list = ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDJPY", "USDCHF", "USDCAD"]

# --- In-memory cache ---
if "mt5_cache" not in st.session_state:
    st.session_state["mt5_cache"] = {}

# --- UI: Show rates ---
st.title("📊 FX Rates from MetaTrader 5")
st.caption("Refreshing every 60 seconds.")

st.sidebar.header("⚙️ Settings")
ema_period = st.sidebar.number_input("EMA Period", min_value=1, max_value=500, value=20, step=1)


# Create empty container
latest_closes = pd.DataFrame(index=fx_list, columns=timeframes.keys())
refreshed_tfs = set() 

for symbol in fx_list:
    for tf_name, tf_code in timeframes.items():
        rates, is_fresh = get_cached_rates(symbol, tf_code, 200)
        
        if is_fresh:
            refreshed_tfs.add(tf_name)

        if rates is None or len(rates) == 0:
            latest_closes.loc[symbol, tf_name] = None
            continue

        df = pd.DataFrame(rates)
        latest_close = df["close"].iloc[-1]
        latest_closes.loc[symbol, tf_name] = round(latest_close, 6)

if refreshed_tfs:
    with st.sidebar.expander("🔁 Refreshed Timeframes", expanded=True):
        st.write(f"⏱ Refreshed at {datetime.now().strftime('%H:%M:%S')}")
        for tf_name in sorted(refreshed_tfs, key=lambda k: list(timeframes.keys()).index(k)):
            st.markdown(f"• {tf_name}")
else:
    with st.sidebar.expander("✔️ All from Cache", expanded=False):
        st.write(f"⏱ Checked at {datetime.now().strftime('%H:%M:%S')}")


st.subheader("📈 Latest Close Prices by Symbol and Timeframe")
st.dataframe(latest_closes, use_container_width=True)

# --- VWAP and EMA Crosses ---
bars_since_df = pd.DataFrame(index=fx_list, columns=timeframes.keys())
direction_map = {}  # to track direction for styling

for symbol in fx_list:
    for tf_name, tf_code in timeframes.items():
        rates, _ = get_cached_rates(symbol, tf_code, 200)  # Get more data for VWAP
        if rates is None or len(rates) < 10:
            bars_since_df.loc[symbol, tf_name] = None
            direction_map[(symbol, tf_name)] = 0
            continue
        
        df = pd.DataFrame(rates)
        typical_price = (df["high"] + df["low"] + df["close"]) / 3
        volume = df["tick_volume"]

        vwap_line = vwap(typical_price.values, volume.values)
        bars_since, direction = bars_since_cross(df["close"].values, vwap_line)

        if bars_since is not None:
            bars_since_df.loc[symbol, tf_name] = bars_since
            direction_map[(symbol, tf_name)] = direction
        else:
            bars_since_df.loc[symbol, tf_name] = 0
            direction_map[(symbol, tf_name)] = 0


styled_bars_df = bars_since_df.style.apply(
    lambda row: [highlight_cross(row[col], row.name, col, direction_map) for col in row.index],
    axis=1
)

st.subheader("📉 Bars Since Last VWAP Cross")
st.dataframe(styled_bars_df, use_container_width=True)


ema_bars_df = pd.DataFrame(index=fx_list, columns=timeframes.keys())
ema_direction_map = {}

for symbol in fx_list:
    for tf_name, tf_code in timeframes.items():
        rates, _ = get_cached_rates(symbol, tf_code, 200)
        if rates is None or len(rates) <= ema_period:
            ema_bars_df.loc[symbol, tf_name] = None
            ema_direction_map[(symbol, tf_name)] = 0
            continue

        df = pd.DataFrame(rates)
        close = df["close"].values
        ema_line = ema(close, ema_period)

        bars_since, direction = bars_since_cross(close, ema_line)

        if bars_since is not None:
            ema_bars_df.loc[symbol, tf_name] = bars_since
            ema_direction_map[(symbol, tf_name)] = direction
        else:
            ema_bars_df.loc[symbol, tf_name] = None
            ema_direction_map[(symbol, tf_name)] = 0

styled_ema_df = ema_bars_df.style.apply(
    lambda row: [highlight_cross(row[col], row.name, col, ema_direction_map) for col in row.index],
    axis=1
)

st.subheader("📉 Bars Since Last EMA Cross")
st.dataframe(styled_ema_df, use_container_width=True)
