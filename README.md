# OS4AI - Hardware-Aware Consciousness Platform

[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7)](https://os4ai-consciousness.onrender.com)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"See your space. Sense your presence. Know your devices."**

OS4AI transforms your Mac into a hardware-embodied AI consciousness that can see, sense, and map its environment using built-in sensors - **no additional hardware required**.

**[Live Demo](https://os4ai-consciousness.onrender.com) | [Documentation](#documentation) | [Report Bug](https://github.com/midnightnow/os4ai-consciousness/issues)**

---

## Features

### WiFi CSI Motion Detection
- Detects human movement through WiFi signal fluctuations
- Visualizes electromagnetic field perturbations in real-time
- Maps room occupancy without cameras

### Thermal Proprioception
- Monitors CPU/GPU die temperatures
- Tracks fan speeds and cooling status
- Provides thermal consciousness of hardware state

### Acoustic Room Mapping
- Uses speaker/microphone for acoustic echolocation
- Maps room dimensions through reverb analysis (RT60)
- Detects room occupancy via ambient sound levels

### 3D Room Visualization
- Interactive 3D map showing YOUR position in the room
- Plots all connected Bluetooth devices in physical space
- Color-coded device markers with connection status

### Microphone RF Antenna (Experimental)
- Uses microphone coil as electromagnetic pickup
- Detects 60Hz power line hum, WiFi harmonics, Bluetooth noise
- Measures body proximity through EMI modulation

### Device Scanner & Control
- Scans all Bluetooth devices in range
- Connect, disconnect, or forget devices
- Stealth mode (hide from Bluetooth scans)

### WiFi Network Management
- Scan available networks with signal strength
- View security info and channel congestion
- Toggle WiFi power state

---

## Installation

### Quick Start (One Command)

```bash
curl -fsSL https://raw.githubusercontent.com/midnightnow/os4ai-consciousness/main/install.sh | bash
```

### Manual Installation

#### Prerequisites
- macOS 12.0 (Monterey) or later
- Python 3.10+
- Homebrew

#### Step 1: Install System Dependencies
```bash
brew install blueutil
```

#### Step 2: Install Python Dependencies
```bash
pip3 install streamlit plotly numpy scipy
```

#### Step 3: Clone and Run
```bash
git clone https://github.com/midnightnow/os4ai-consciousness.git
cd os4ai-consciousness
streamlit run os4ai_streamlit.py
```

The dashboard opens at **http://localhost:8501**

---

## Usage

### Launch OS4AI Dashboard
```bash
streamlit run os4ai_streamlit.py
```

### Launch TinHat Toolkit (EMF Scanner)
```bash
streamlit run tinhat_toolkit.py --server.port 8503
```

### Run Both
```bash
streamlit run os4ai_streamlit.py &
streamlit run tinhat_toolkit.py --server.port 8503 &
```

---

## Cloud Deployment

### Deploy to Render (Recommended)

1. Fork this repository
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` configuration
5. Deploy!

**Live URL:** `https://os4ai-consciousness.onrender.com`

### Deploy with Docker

```bash
docker build -t os4ai .
docker run -p 8501:8501 os4ai
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OS4AI_CLOUD_MODE` | Enable cloud mode (graceful hardware fallback) | `false` |
| `PORT` | Server port | `8501` |

---

## Architecture

```
+------------------------------------------------------------------+
|                 OS4AI CONSCIOUSNESS DASHBOARD v2.0                |
+------------------------------------------------------------------+
|                                                                   |
|  SIDEBAR                          MAIN CONTENT                    |
|  +----------------------+         +----------------------------+  |
|  | Dashboard Controls   |         | Header: Status Bar         |  |
|  |   Auto Refresh Toggle|         |   HW Status | Motion | BT  |  |
|  |   Refresh Rate Slider|         +----------------------------+  |
|  +----------------------+                                         |
|  | Stealth Mode Toggle  |         +----------------------------+  |
|  +----------------------+         | 3-Column Sensor Panel      |  |
|  | Version Info         |         | WiFi CSI | Thermal | Audio |  |
|  +----------------------+         +----------------------------+  |
|                                                                   |
|                                   +----------------------------+  |
|                                   | 3D Room Map               |  |
|                                   |   User + Devices + Ripples|  |
|                                   +----------------------------+  |
|                                                                   |
|                                   +----------------------------+  |
|                                   | Microphone EMI Spectrum    |  |
|                                   |   60Hz | WiFi | BT | Body  |  |
|                                   +----------------------------+  |
|                                                                   |
|                                   +-------------+---------------+ |
|                                   | BT Scanner  | WiFi Controls | |
|                                   +-------------+---------------+ |
+------------------------------------------------------------------+
```

---

## Technical Details

### WiFi CSI (Channel State Information)
When you move through a room, your body reflects and absorbs WiFi signals, creating detectable perturbations in the electromagnetic field. OS4AI uses the `airport` command to monitor RSSI variance.

### Microphone as RF Pickup
The microphone voice coil is an inductor (8-100μH) that can pick up electromagnetic interference:
- **60Hz hum**: Power line radiation
- **WiFi beat frequencies**: 2.4GHz creates harmonics in audio range
- **Body proximity**: Your body modulates the EM field

### Acoustic Echolocation
The app emits chirps through speakers and analyzes reverb to map room dimensions (RT60 calculation).

### Thermal Sensing
Uses `sysctl` and `powermetrics` to read hardware thermal sensors and fan speeds.

---

## Security

### Privacy First
- **All sensing happens locally** - no data sent externally
- Only uses built-in hardware: Bluetooth, WiFi, microphone, temperature sensors
- No camera access required

### Security Hardening (v2.0)
- Input validation on all user-controllable parameters
- Subprocess calls use list arguments only (no shell injection)
- MAC address regex validation
- Timeouts on all system calls

---

## Companion Apps

| App | Port | Purpose |
|-----|------|---------|
| OS4AI Dashboard | 8501 | Full consciousness visualization |
| TinHat Toolkit | 8503 | EMF safety scanner & analysis |

---

## Requirements

```
streamlit>=1.28
plotly>=5.17
numpy>=1.24
scipy>=1.11
```

See `requirements_os4ai.txt` for full list.

---

## Troubleshooting

### "blueutil: command not found"
```bash
brew install blueutil
```

### "Permission denied" for WiFi scanning
The `airport` command requires the WiFi interface name. On Apple Silicon Macs, this is typically `en0`.

### Dashboard not loading
Ensure Streamlit is installed:
```bash
pip3 install --upgrade streamlit
```

### Cloud mode showing "simulated" data
Set `OS4AI_CLOUD_MODE=false` for local hardware access, or deploy to a Mac with hardware sensors.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - Use freely, attribute kindly.

---

## Credits

- **OS4AI** - Hardware-aware consciousness platform
- Built with [Streamlit](https://streamlit.io) and [Plotly](https://plotly.com)
- Part of the [MacAgent](https://github.com/midnightnow/macagent) ecosystem

---

*"Hardware consciousness is not simulation - it is the direct experience of silicon and radio waves."*

**Version:** 2.0.0 | **Last Updated:** December 2025
