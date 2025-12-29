#!/usr/bin/env python3
"""
TINHAT TOOLKIT - EMF Safety Scanner & Device Detector
"See the invisible. Protect what matters."

A standalone app for privacy-conscious users who want to know
what's emitting electromagnetic radiation in their space.

Launch: streamlit run tinhat_toolkit.py
"""

__version__ = "1.0.0"
__author__ = "Tinhat Project"
__license__ = "MIT"

import streamlit as st
import subprocess
import json
import time
from datetime import datetime, timedelta
from collections import deque
import os

# Page config
st.set_page_config(
    page_title="Tinhat Toolkit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean, professional look
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    .device-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        backdrop-filter: blur(10px);
    }
    .device-card-warning {
        background: rgba(255,100,100,0.1);
        border: 1px solid rgba(255,100,100,0.3);
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
    }
    .metric-box {
        background: rgba(0,255,136,0.1);
        border: 1px solid rgba(0,255,136,0.3);
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }
    .safe { color: #00ff88; }
    .warning { color: #ffaa00; }
    .danger { color: #ff4444; }
    h1, h2, h3 { color: #ffffff !important; }
    .stMetric label { color: #888 !important; }
    .stMetric [data-testid="stMetricValue"] { color: #00ff88 !important; }
</style>
""", unsafe_allow_html=True)

# Session state for history
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []
if 'exposure_log' not in st.session_state:
    st.session_state.exposure_log = deque(maxlen=100)
if 'headset_on_body_start' not in st.session_state:
    st.session_state.headset_on_body_start = None

# ==================== DEVICE SCANNING ====================

@st.cache_data(ttl=10, show_spinner=False)
def scan_bluetooth_devices():
    """Scan for Bluetooth devices using system_profiler (cached 10s)"""
    try:
        result = subprocess.run(
            ['system_profiler', 'SPBluetoothDataType'],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout

        devices = []
        lines = output.split('\n')
        current_device = {}
        in_connected = False
        current_name = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            if 'Connected:' in line and 'Not Connected' not in line:
                in_connected = True
            elif 'Not Connected:' in line:
                in_connected = False
            elif stripped.endswith(':') and 'Address' not in stripped and 'Battery' not in stripped:
                # This might be a device name
                current_name = stripped[:-1]
            elif 'Address:' in line:
                addr = line.split('Address:')[-1].strip()
                current_device = {
                    'address': addr,
                    'connected': in_connected,
                    'name': current_name or 'Unknown Device'
                }
            elif 'Minor Type:' in line:
                current_device['type'] = line.split(':')[-1].strip()
                if current_device.get('address'):
                    devices.append(current_device.copy())
                current_device = {}
            elif 'Battery Level:' in line:
                current_device['battery'] = line.split(':')[-1].strip()

        return devices
    except Exception as e:
        return []

@st.cache_data(ttl=15, show_spinner=False)
def scan_wifi_networks():
    """Scan for nearby WiFi networks (cached 15s)"""
    try:
        # Try using CoreWLAN via system command
        result = subprocess.run(
            ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'],
            capture_output=True, text=True, timeout=10
        )

        networks = []
        lines = result.stdout.strip().split('\n')[1:]  # Skip header

        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                ssid = parts[0] if parts[0] else '<Hidden>'
                rssi = int(parts[1]) if parts[1].lstrip('-').isdigit() else -100
                networks.append({
                    'ssid': ssid,
                    'rssi': rssi,
                    'signal_quality': min(100, max(0, (rssi + 100) * 2))
                })

        return sorted(networks, key=lambda x: x['rssi'], reverse=True)[:10]
    except:
        return []

def estimate_distance_from_rssi(rssi, tx_power=-59):
    """Estimate distance from RSSI using log-distance path loss model"""
    if rssi == 0:
        return -1
    ratio = (tx_power - rssi) / (10 * 2.0)  # n=2 for free space
    return round(10 ** ratio, 1)

def get_emf_exposure_level(devices):
    """Calculate EMF exposure estimate based on connected devices"""
    connected = [d for d in devices if d.get('connected')]

    # Weight different device types
    exposure = 0
    for device in connected:
        dtype = device.get('type', '').lower()
        if 'headset' in dtype or 'headphone' in dtype:
            exposure += 3  # Near head = higher concern
        elif 'watch' in dtype:
            exposure += 2  # On body
        elif 'phone' in dtype:
            exposure += 2
        else:
            exposure += 1

    if exposure <= 2:
        return ("LOW", "safe", "✅")
    elif exposure <= 5:
        return ("MODERATE", "warning", "⚠️")
    else:
        return ("HIGH", "danger", "🔴")

# ==================== UI ====================

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/privacy.png", width=80)
    st.title("🛡️ Tinhat Toolkit")
    st.markdown("*EMF Safety Scanner*")
    st.markdown("---")

    # Settings
    st.subheader("⚙️ Settings")
    scan_interval = st.slider("Scan interval (seconds)", 2, 30, 5)
    show_wifi = st.checkbox("Show WiFi Networks", value=True)
    show_alerts = st.checkbox("Show Safety Alerts", value=True)
    headset_alert_mins = st.slider("Headset alert after (mins)", 15, 120, 30)

    st.markdown("---")

    # Export
    st.subheader("📊 Export Report")
    if st.button("Generate PDF Report"):
        st.info("Report generation coming soon!")

    if st.button("Export to JSON"):
        report = {
            'timestamp': datetime.now().isoformat(),
            'devices': scan_bluetooth_devices(),
            'exposure_history': list(st.session_state.exposure_log)
        }
        st.download_button(
            "Download JSON",
            json.dumps(report, indent=2),
            file_name=f"tinhat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Main content
st.title("🛡️ Tinhat Toolkit")
st.markdown("### *See the invisible. Protect what matters.*")

# Scan devices
devices = scan_bluetooth_devices()
wifi_networks = scan_wifi_networks() if show_wifi else []

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_devices = len(devices)
    st.metric("📡 Total Devices", total_devices)

with col2:
    connected = len([d for d in devices if d.get('connected')])
    st.metric("🔗 Connected", connected)

with col3:
    level, style, icon = get_emf_exposure_level(devices)
    st.metric(f"EMF Exposure {icon}", level)

with col4:
    wifi_count = len(wifi_networks)
    st.metric("📶 WiFi Networks", wifi_count)

st.markdown("---")

# Device sections
tab1, tab2, tab3, tab4 = st.tabs(["🔗 Connected Devices", "📡 Nearby Devices", "📶 WiFi Networks", "📈 Exposure History"])

with tab1:
    st.subheader("🔗 Devices Connected to Your Mac")

    connected_devices = [d for d in devices if d.get('connected')]

    if connected_devices:
        for device in connected_devices:
            dtype = device.get('type', 'Unknown')
            name = device.get('name', 'Unknown')
            battery = device.get('battery', 'N/A')

            # Device icons
            icons = {
                'Keyboard': '⌨️',
                'Mouse': '🖱️',
                'Headset': '🎧',
                'Headphones': '🎧',
                'Watch': '⌚',
                'Phone': '📱',
                'Speaker': '🔊',
            }
            icon = icons.get(dtype, '📡')

            # Distance estimate
            if dtype in ['Keyboard', 'Mouse']:
                distance = "~0.5m (desk)"
                risk = "low"
            elif dtype in ['Headset', 'Headphones']:
                distance = "~0.1m (ON HEAD)"
                risk = "monitor"

                # Track time on body
                if st.session_state.headset_on_body_start is None:
                    st.session_state.headset_on_body_start = datetime.now()
            elif dtype == 'Watch':
                distance = "~0m (ON BODY)"
                risk = "monitor"
            else:
                distance = "<2m"
                risk = "low"

            # Card styling based on risk
            card_class = "device-card-warning" if risk == "monitor" else "device-card"

            st.markdown(f"""
            <div class="{card_class}">
                <span style="font-size: 32px;">{icon}</span>
                <strong style="font-size: 18px; color: white;">{dtype}</strong>
                <span style="color: #888;">({name})</span><br>
                <span style="color: #00ff88;">📍 {distance}</span> |
                <span style="color: #888;">🔋 {battery}</span>
            </div>
            """, unsafe_allow_html=True)

            # Headset time tracking
            if dtype in ['Headset', 'Headphones'] and st.session_state.headset_on_body_start:
                duration = datetime.now() - st.session_state.headset_on_body_start
                mins = int(duration.total_seconds() / 60)
                if mins >= headset_alert_mins and show_alerts:
                    st.warning(f"🎧 Headset on head for {mins} minutes! Consider a break for ear health.")
    else:
        st.info("No devices currently connected via Bluetooth.")
        st.session_state.headset_on_body_start = None

with tab2:
    st.subheader("📡 Nearby Bluetooth Devices (Not Connected)")

    nearby = [d for d in devices if not d.get('connected')]

    if nearby:
        for device in nearby:
            dtype = device.get('type', 'Unknown')
            addr = device.get('address', 'Unknown')[:8] + '...'

            icons = {
                'Video Display': '📺',
                'Laptop Computer': '💻',
                'Phone': '📱',
                'Speaker': '🔊',
                'Tablet': '📱',
            }
            icon = icons.get(dtype, '📡')

            st.markdown(f"""
            <div class="device-card">
                <span style="font-size: 24px;">{icon}</span>
                <span style="color: #888;">{dtype}</span>
                <span style="color: #555; font-size: 12px;">({addr})</span><br>
                <span style="color: #666;">📍 2-10m (estimated)</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No nearby Bluetooth devices detected.")

with tab3:
    st.subheader("📶 WiFi Networks in Range")

    if wifi_networks:
        for network in wifi_networks:
            ssid = network['ssid']
            rssi = network['rssi']
            quality = network['signal_quality']
            distance = estimate_distance_from_rssi(rssi)

            # Signal strength color
            if quality > 70:
                color = "#00ff88"
                strength = "Strong"
            elif quality > 40:
                color = "#ffaa00"
                strength = "Medium"
            else:
                color = "#ff4444"
                strength = "Weak"

            st.markdown(f"""
            <div class="device-card">
                <span style="font-size: 20px;">📶</span>
                <strong style="color: white;">{ssid}</strong><br>
                <span style="color: {color};">Signal: {rssi} dBm ({strength})</span> |
                <span style="color: #888;">~{distance}m away</span>
                <div style="background: #333; border-radius: 4px; height: 8px; margin-top: 5px;">
                    <div style="background: {color}; width: {quality}%; height: 100%; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("WiFi scanning not available or disabled.")

with tab4:
    st.subheader("📈 EMF Exposure History")

    # Log current exposure
    level, _, _ = get_emf_exposure_level(devices)
    st.session_state.exposure_log.append({
        'time': datetime.now().isoformat(),
        'level': level,
        'device_count': len([d for d in devices if d.get('connected')])
    })

    if st.session_state.exposure_log:
        # Simple visualization
        import plotly.graph_objects as go

        times = [entry['time'][-8:-3] for entry in st.session_state.exposure_log]
        counts = [entry['device_count'] for entry in st.session_state.exposure_log]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(counts))),
            y=counts,
            mode='lines+markers',
            line=dict(color='#00ff88', width=2),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(0,255,136,0.2)'
        ))
        fig.update_layout(
            title="Connected Devices Over Time",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0.3)',
            font=dict(color='white'),
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=False, title="Time"),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title="Devices")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Exposure history will appear here as you use the app.")

# Safety Tips
st.markdown("---")
with st.expander("🛡️ EMF Safety Tips", expanded=False):
    st.markdown("""
    ### Reduce Your EMF Exposure

    1. **Headphones/Headsets**: Take breaks every 30 minutes
    2. **WiFi Router**: Keep 6+ feet away from where you sleep
    3. **Smartwatch**: Remove during sleep
    4. **Phone**: Don't keep in pocket - use a bag
    5. **Laptop**: Use on desk, not on lap

    ### When to Be Concerned
    - Multiple devices constantly on body
    - Headphones worn 8+ hours daily
    - Sleeping next to phone/router

    ### This Tool Helps By
    - Showing all emitting devices near you
    - Tracking time devices are on your body
    - Alerting when exposure may be high
    """)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 12px;">
    🛡️ Tinhat Toolkit v1.0 | Last scan: {datetime.now().strftime('%H:%M:%S')} |
    <a href="#" style="color: #00ff88;">Privacy Policy</a>
</div>
""", unsafe_allow_html=True)

# Auto-refresh
time.sleep(scan_interval)
st.rerun()
