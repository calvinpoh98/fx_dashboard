import streamlit as st
import MetaTrader5 as mt

def init_login():
    if "mt5_logged_in" not in st.session_state:
        st.session_state["mt5_logged_in"] = False

    if "mt5_credentials" not in st.session_state:
        st.session_state["mt5_credentials"] = {
            "login": None,
            "password": None,
            "server": None
        }

    st.sidebar.header("🔐 MT5 Login")

    if not st.session_state["mt5_logged_in"]:
        login = st.sidebar.text_input("Login", value=st.session_state["mt5_credentials"]["login"] or "144938")
        password = st.sidebar.text_input("Password", type="password", value=st.session_state["mt5_credentials"]["password"] or "")
        server = st.sidebar.text_input("Server", value=st.session_state["mt5_credentials"]["server"] or "FusionMarkets-Demo")

        connect_btn = st.sidebar.button("Connect to MetaTrader 5")

        if connect_btn:
            try:
                login_int = int(login)
                if mt.initialize(login=login_int, password=password, server=server):
                    st.session_state["mt5_logged_in"] = True
                    st.session_state["mt5_credentials"] = {
                        "login": login,
                        "password": password,
                        "server": server
                    }
                    st.sidebar.success("✅ Connected to MetaTrader 5")
                    st.rerun()

                else:
                    st.sidebar.error("❌ Failed to connect to MetaTrader 5")
            except Exception as e:
                st.sidebar.error(f"⚠️ Error: {e}")
    else:
        creds = st.session_state["mt5_credentials"]
        st.sidebar.markdown(f"👤 **Logged in as {creds['login']}**")
        st.sidebar.markdown(f"🌐 **Server:** {creds['server']}")

    # Always show disconnect button
    if st.session_state["mt5_logged_in"]:
        if st.sidebar.button("Disconnect"):
            mt.shutdown()
            st.session_state["mt5_logged_in"] = False
            st.sidebar.info("🔌 Disconnected")
            st.rerun()


    return st.session_state["mt5_logged_in"]
