import MetaTrader5 as mt
from datetime import datetime
import streamlit as st

# --- Rate fetcher with per-timeframe TTL ---
PER_TF_TTL = {
    mt.TIMEFRAME_M1: 60,
    mt.TIMEFRAME_M5: 60,
    mt.TIMEFRAME_M15: 300,
    mt.TIMEFRAME_M30: 600,
    mt.TIMEFRAME_H1: 900,
    mt.TIMEFRAME_H4: 3600,
    mt.TIMEFRAME_D1: 86400,
}

def get_cached_rates(symbol, timeframe, pos=200):
    key = (symbol, timeframe)
    ttl = PER_TF_TTL[timeframe]
    now = datetime.now()

    CACHE = st.session_state["mt5_cache"]

    if key in CACHE:
        cached_time, data = CACHE[key]
        if (now - cached_time).total_seconds() < ttl:
            return data, False  # False = from cache

    rates = mt.copy_rates_from_pos(symbol, timeframe, 0, pos)
    if rates is None:
        return None, False

    CACHE[key] = (now, rates)
    return rates, True