import streamlit as st
import pandas as pd
import requests
import json
import websocket
import threading
from streamlit_autorefresh import st_autorefresh

# 1. High-Performance Responsive UI Configuration
st.set_page_config(page_title="THEFXEMPIRE // TERMINAL", layout="wide", initial_sidebar_state="expanded")

# Injecting Custom Glass-Cyan CSS Framework (Transparent Tables & Background Sync)
st.markdown("""
    <style>
        /* Global Responsive Deep Cosmic/Cyan Gradient Background */
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #060B13 0%, #0A192F 50%, #051B2C 100%) !important;
            background-attachment: fixed !important;
            color: #E2E8F0 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Modernized Header Block */
        [data-testid="stHeader"] {
            background: rgba(11, 19, 36, 0.5) !important;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0, 245, 255, 0.1);
        }

        /* Sidebar Glassmorphism Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(11, 20, 38, 0.95) !important;
            border-right: 1px solid rgba(0, 245, 255, 0.15) !important;
            box-shadow: 4px 0 25px rgba(0, 0, 0, 0.4);
        }
        
        /* Persistent Platform Identity Panel */
        .sidebar-logo {
            font-family: 'Courier New', Courier, monospace;
            font-size: 16px;
            font-weight: 900;
            color: #00F5FF;
            letter-spacing: 2px;
            text-align: center;
            padding: 12px;
            border: 1px solid rgba(0, 245, 255, 0.3);
            border-radius: 6px;
            margin-bottom: 25px;
            background: rgba(0, 245, 255, 0.05);
            backdrop-filter: blur(5px);
            box-shadow: 0 0 15px rgba(0, 245, 255, 0.1);
        }
        
        /* Master Branding Header - Radiant Cyan */
        .brand-header {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            font-size: clamp(22px, 4vw, 32px); /* Responsive sizing fluid typography */
            font-weight: 800;
            letter-spacing: 2px;
            color: #FFFFFF;
            background: linear-gradient(90deg, #FFFFFF, #00F5FF, #00BFFF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding-bottom: 4px;
            margin-bottom: 5px;
        }
        .brand-subheader {
            font-size: clamp(10px, 2vw, 12px);
            color: #64748B;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 30px;
            border-bottom: 1px solid rgba(0, 245, 255, 0.15);
            padding-bottom: 10px;
        }

        /* Flexible Order Book Framework */
        .ladder-header { 
            font-weight: 700; 
            text-align: center; 
            padding: 10px; 
            background: rgba(16, 28, 48, 0.8);
            border: 1px solid rgba(0, 245, 255, 0.2);
            border-radius: 4px 4px 0 0;
            font-size: 11px;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #00F5FF;
        }
        .bid-cell { 
            background-color: rgba(0, 245, 255, 0.04); 
            color: #00F5FF; 
            text-align: center; 
            font-family: 'SFMono-Regular', Consolas, monospace; 
            font-weight: 600;
            padding: 6px; 
            border: 1px solid rgba(0, 245, 255, 0.08); 
            font-size: 12px; 
        }
        .ask-cell { 
            background-color: rgba(255, 69, 96, 0.04); 
            color: #FF4560; 
            text-align: center; 
            font-family: 'SFMono-Regular', Consolas, monospace; 
            font-weight: 600;
            padding: 6px; 
            border: 1px solid rgba(255, 69, 96, 0.08); 
            font-size: 12px; 
        }
        .price-cell { 
            background: rgba(26, 38, 57, 0.9);
            color: #FFFFFF; 
            font-weight: 700; 
            text-align: center; 
            font-family: 'SFMono-Regular', Consolas, monospace; 
            padding: 6px; 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            font-size: 12px; 
        }
        .empty-cell { 
            background-color: rgba(10, 17, 30, 0.5); 
            border: 1px solid rgba(255, 255, 255, 0.03); 
        }
        
        /* Premium Response Component Grid Cards */
        .metric-card {
            background: rgba(15, 27, 46, 0.7);
            border: 1px solid rgba(0, 245, 255, 0.1);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            backdrop-filter: blur(12px);
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .metric-card:hover {
            border: 1px solid #00F5FF;
            box-shadow: 0 0 15px rgba(0, 245, 255, 0.2);
            transform: translateY(-2px);
        }
        .metric-label { font-size: 10px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px; }
        .metric-value { font-size: 20px; font-weight: 700; font-family: monospace; }
        
        /* Clean & Professional Transparent Table System (Overwriting Black Backgrounds) */
        div[data-testid="stDataFrame"], 
        div[data-testid="stDataFrame"] > div, 
        div[data-testid="stDataFrame"] iframe {
            background-color: transparent !important;
            background: transparent !important;
        }
        
        div[data-testid="stDataFrame"] [data-testid="StyledDataTable"] {
            background-color: transparent !important;
            border: none !important;
        }

        div[data-testid="stDataFrame"] th {
            background-color: rgba(16, 28, 48, 0.6) !important;
            color: #00F5FF !important;
            font-size: 11px !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            border-bottom: 1px solid rgba(0, 245, 255, 0.2) !important;
        }

        div[data-testid="stDataFrame"] td {
            background-color: transparent !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            font-size: 12px !important;
            color: #E2E8F0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Auto-refresh cycle handling live data updates
st_autorefresh(interval=400, limit=10000, key="dynamic_matrix_sync")

# --- INITIALIZE GLOBAL SHARED STORAGE ---
@st.cache_resource
def get_shared_market_memory():
    return {
        "dom_books": {},        
        "active_threads": {},   
        "ws_status": {}         
    }

shared_memory = get_shared_market_memory()

# --- ASSET WATCHLIST POOL DEFINITIONS ---
ASSET_POOL = {
    "🌐 CRYPTO CORE": ["BTCUSDT", "ETHUSDT"],
    "🚀 HIGH-BETA ALTS": ["SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "LINKUSDT"],
    "💱 FIAT STABLE CROSSES": ["EURUSDT", "JPYUSDT"]
}

DECIMAL_MAP = {
    "BTCUSDT": 1, "ETHUSDT": 2, "SOLUSDT": 2, "BNBUSDT": 2, "XRPUSDT": 4, "ADAUSDT": 4, "LINKUSDT": 3,
    "EURUSDT": 5, "JPYUSDT": 5
}

# --- GLOBAL SIDEBAR NAVIGATION ENGINE & PERSISTENT LOGO ---
st.sidebar.markdown('<div class="sidebar-logo">⚡ THEFXEMPIRE</div>', unsafe_allow_html=True)

st.sidebar.markdown("### 🛠️ CORE CONFIG ENGINE")
selected_watchlist = []
for category, tokens in ASSET_POOL.items():
    st.sidebar.markdown(f"**{category}**")
    for token in tokens:
        is_default = token in ["BTCUSDT", "SOLUSDT", "EURUSDT"]
        if st.sidebar.checkbox(f"Track {token}", value=is_default, key=f"check_{token}"):
            selected_watchlist.append(token)

if not selected_watchlist:
    selected_watchlist = ["BTCUSDT"]

# 2. REST Data API Node (Calculates Scanner Metrics)
@st.cache_data(ttl=30)
def calculate_atr_metrics(symbol, lookback=14, timeframe="1h"):
    try:
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={timeframe}&limit={lookback + 1}"
        response = requests.get(url).json()
        
        df = pd.DataFrame(response, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume', 
            'close_time', 'asset_volume', 'trades', 'taker_base', 'taker_quote', 'ignored'
        ])
        
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        
        df['prev_close'] = df['close'].shift(1)
        df['tr1'] = df['high'] - df['low']
        df['tr2'] = (df['high'] - df['prev_close']).abs()
        df['tr3'] = (df['low'] - df['prev_close']).abs()
        df['true_range'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
        
        atr_value = df['true_range'].rolling(window=lookback).mean().iloc[-1]
        current_price = df['close'].iloc[-1]
        atr_pct = (atr_value / current_price) * 100
        
        return current_price, atr_value, round(atr_pct, 2)
    except:
        return 0.0, 0.0, 0.0

# 3. Stream Mode WebSocket Node
def open_dom_socket(symbol):
    sym = symbol.lower()
    socket_url = f"wss://fstream.binance.com/public/stream?streams={sym}@depth20@100ms"
    
    def on_open(ws):
        shared_memory["ws_status"][sym] = "CONNECTED_STREAMING"

    def on_message(ws, message):
        try:
            payload = json.loads(message)
            data = payload.get("data", payload)
            
            raw_bids = data.get("b", [])
            raw_asks = data.get("a", [])
            
            bids_dict = {float(item[0]): float(item[1]) for item in raw_bids}
            asks_dict = {float(item[0]): float(item[1]) for item in raw_asks}
            
            shared_memory["dom_books"][sym] = {"bids": bids_dict, "asks": asks_dict}
            shared_memory["ws_status"][sym] = "ACTIVE"
        except Exception as e:
            shared_memory["ws_status"][sym] = f"PARSE_ERR: {str(e)}"

    def on_error(ws, error):
        shared_memory["ws_status"][sym] = f"CONN_ERROR: {str(error)}"

    def on_close(ws, close_status_code, close_msg):
        shared_memory["ws_status"][sym] = "DISCONNECTED"

    ws = websocket.WebSocketApp(
        socket_url, 
        on_open=on_open,
        on_message=on_message, 
        on_error=on_error, 
        on_close=on_close
    )
    ws.run_forever()

# --- START BACKGROUND NODES FOR ALL TRACKED ASSETS ---
for pair in selected_watchlist:
    t_lower = pair.lower()
    if t_lower not in shared_memory["active_threads"] or not shared_memory["active_threads"][t_lower].is_alive():
        shared_memory["dom_books"][t_lower] = {"bids": {}, "asks": {}}
        shared_memory["ws_status"][t_lower] = "BOOTING_NODE..."
        t = threading.Thread(target=open_dom_socket, args=(pair,), daemon=True)
        t.start()
        shared_memory["active_threads"][t_lower] = t

# --- MASTER BRAND HEADING ---
st.markdown('<div class="brand-header">THEFXEMPIRE TERMINAL</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subheader">REAL-TIME INSTITUTIONAL LIQUIDITY MATRIX // RESPONSIVE SKY CYAN VIEW</div>', unsafe_allow_html=True)

# --- PANEL DISPLAY BUILD (RESPONSIVE GRID) ---
left_panel, right_panel = st.columns([1.2, 1], gap="large")

with left_panel:
    st.markdown("##### 🔍 SYSTEM MATRIX MONITOR")
    
    scanner_records = []
    for pair in selected_watchlist:
        price, atr, atr_pct = calculate_atr_metrics(pair)
        dec = DECIMAL_MAP.get(pair, 2)
        
        t_lower = pair.lower()
        book = shared_memory["dom_books"].get(t_lower, {"bids": {}, "asks": {}})
        bids = book.get("bids", {})
        asks = book.get("asks", {})
        
        total_bid_sz = sum(bids.values())
        total_ask_sz = sum(asks.values())
        total_depth = total_bid_sz + total_ask_sz
        
        if total_depth > 0:
            imbalance_val = ((total_bid_sz - total_ask_sz) / total_depth) * 100
            imbalance_str = f"🔷 +{imbalance_val:.0f}%" if imbalance_val >= 0 else f"🔶 {imbalance_val:.0f}%"
        else:
            imbalance_str = "SYNCING..."
            
        void_alert = "NORMAL"
        if total_depth > 0:
            if (total_bid_sz / total_depth) < 0.15:
                void_alert = "🚨 BID VOID"
            elif (total_ask_sz / total_depth) < 0.15:
                void_alert = "🚨 ASK VOID"

        scanner_records.append({
            "Asset": pair,
            "Price": f"{price:.{dec}f}" if price > 0 else "0.00",
            "Volatility (ATR)": f"{atr_pct}%",
            "DOM Imbalance": imbalance_str,
            "State": void_alert
        })
        
    # Build clean dataframe view without background wrapping layout blocks
    scanner_df = pd.DataFrame(scanner_records)
    st.dataframe(scanner_df, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    selected_target = st.selectbox("ROUTED DOM MATRIX TARGET SELECTION:", selected_watchlist, index=0)
    target_lower = selected_target.lower()

with right_panel:
    st.markdown(f"##### 📊 DEPTH FLOW LADDER: {selected_target}")
    
    active_book = shared_memory["dom_books"].get(target_lower, {"bids": {}, "asks": {}})
    bids = active_book.get("bids", {})
    asks = active_book.get("asks", {})
    
    t_bid_sz = sum(bids.values())
    t_ask_sz = sum(asks.values())
    t_total = t_bid_sz + t_ask_sz
    imb_pct = ((t_bid_sz - t_ask_sz) / t_total * 100) if t_total > 0 else 0
    
    # Grid Layout for Analytics Cards
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Bids</div><div class="metric-value" style="color: #00F5FF;">{t_bid_sz:.2f}</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Asks</div><div class="metric-value" style="color: #FF4560;">{t_ask_sz:.2f}</div></div>', unsafe_allow_html=True)
    with m3:
        color = "#00F5FF" if imb_pct >= 0 else "#FF4560"
        st.markdown(f'<div class="metric-card"><div class="metric-label">Net Imbalance</div><div class="metric-value" style="color: {color};">{imb_pct:.1f}%</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not bids and not asks:
        current_status = shared_memory["ws_status"].get(target_lower, "INITIALIZING")
        st.markdown(f'<div style="color:#64748B; font-family:monospace; text-align:center;">NODE NETWORK STATUS // {current_status}</div>', unsafe_allow_html=True)
    else:
        dec_places = DECIMAL_MAP.get(selected_target, 2)
        
        sorted_asks = sorted(list(asks.keys()))[:8]
        sorted_asks.reverse()
        sorted_bids = sorted(list(bids.keys()), reverse=True)[:8]
        all_ladder_prices = sorted_asks + sorted_bids
        
        h1, h2, h3 = st.columns([1, 1.2, 1])
        h1.markdown('<div class="ladder-header" style="color: #00F5FF;">Bids Size</div>', unsafe_allow_html=True)
        h2.markdown('<div class="ladder-header" style="color: #FFFFFF;">Price</div>', unsafe_allow_html=True)
        h3.markdown('<div class="ladder-header" style="color: #FF4560;">Asks Size</div>', unsafe_allow_html=True)
        
        for price in all_ladder_prices:
            c1, c2, c3 = st.columns([1, 1.2, 1])
            c2.markdown(f'<div class="price-cell">{price:.{dec_places}f}</div>', unsafe_allow_html=True)
            
            if price in bids:
                c1.markdown(f'<div class="bid-cell">{bids[price]:.3f}</div>', unsafe_allow_html=True)
                c3.markdown('<div class="empty-cell" style="height:31px; border: 1px solid rgba(255,255,255,0.02);"></div>', unsafe_allow_html=True)
            elif price in asks:
                c1.markdown('<div class="empty-cell" style="height:31px; border: 1px solid rgba(255,255,255,0.02);"></div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="ask-cell">{asks[price]:.3f}</div>', unsafe_allow_html=True)