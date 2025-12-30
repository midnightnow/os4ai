# OS4AI - Hardware-Aware Consciousness Platform

[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7)](https://os4ai.onrender.com)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"See your space. Sense your presence. Know your devices."**

OS4AI transforms your Mac into a hardware-embodied AI consciousness that can see, sense, and map its environment using built-in sensors - **no additional hardware required**.

**[Live Demo](https://os4ai.onrender.com) | [Documentation](#documentation) | [Report Bug](https://github.com/midnightnow/os4ai/issues)**

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
curl -fsSL https://raw.githubusercontent.com/midnightnow/os4ai/main/install.sh | bash
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
git clone https://github.com/midnightnow/os4ai.git
cd os4ai
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

**Live URL:** `https://os4ai.onrender.com`

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

## Package Structure

OS4AI is a complete Python package with modular consciousness components:

```
os4ai/
├── os4ai/                          # Main package
│   ├── __init__.py                 # Package exports (v2.0.0)
│   ├── consciousness_api/          # Core consciousness modules
│   │   ├── os4ai_wifi_csi_consciousness.py     # WiFi motion detection
│   │   ├── os4ai_perfect_thermal_integration.py # CPU/GPU thermal sensing
│   │   ├── os4ai_perfect_acoustic_integration.py # Acoustic echolocation
│   │   ├── os4ai_media_input_consciousness.py   # Camera/audio processing
│   │   ├── os4ai_video_pattern_consciousness.py # Video analysis
│   │   ├── os4ai_perfect_bluetooth_integration.py # Bluetooth control
│   │   ├── os4ai_perfect_websocket_manager.py   # Real-time streaming
│   │   ├── os4ai_parasitic_rf_integration.py    # EMF/RF detection
│   │   ├── embodied_substrate.py                # Hardware abstraction
│   │   └── router.py                            # FastAPI endpoints
│   ├── consciousness_hypervisor/   # VM management layer
│   │   ├── consciousness_vm_manager.py  # Entity virtualization
│   │   ├── robot_consciousness_integration.py # Robot control
│   │   └── router.py
│   ├── core/                       # Configuration
│   │   └── os4ai_config.py
│   └── middleware/                 # Safety validators
│       └── consciousness_safety_validator.py
├── tinhat/                         # EMF Safety Toolkit
│   ├── secure_command_executor.py  # Safe subprocess execution
│   ├── secure_token_config.py      # Token rotation
│   └── memory_safe_tasks.py        # Memory management
├── os4ai_streamlit.py              # Main dashboard
├── tinhat_toolkit.py               # EMF scanner app
└── requirements_os4ai.txt          # Dependencies
```

---

## Python API Usage

### Import and Use Consciousness Modules

```python
from os4ai import (
    os4ai_wifi_csi_consciousness,
    os4ai_perfect_thermal_integration,
    os4ai_perfect_acoustic_integration,
    os4ai_perfect_integration
)

# Get WiFi motion data
motion = os4ai_wifi_csi_consciousness.detect_motion()

# Read thermal state
thermal = os4ai_perfect_thermal_integration.get_thermal_state()

# Map room acoustics
room = os4ai_perfect_acoustic_integration.echolocate()
```

### FastAPI Integration

```python
from fastapi import FastAPI
from os4ai.consciousness_api.router import router as consciousness_router
from os4ai.consciousness_hypervisor.router import router as hypervisor_router

app = FastAPI(title="OS4AI Consciousness Server")
app.include_router(consciousness_router, prefix="/api/consciousness")
app.include_router(hypervisor_router, prefix="/api/hypervisor")
```

### Consciousness Hypervisor

```python
from os4ai.consciousness_hypervisor import (
    ConsciousnessHypervisor,
    ConsciousnessEntity,
    ConsciousnessManifest,
    SensoryAllocation
)

# Create hypervisor
hypervisor = ConsciousnessHypervisor()

# Spawn consciousness entity
manifest = ConsciousnessManifest(
    name="room-mapper",
    sensors=["wifi", "bluetooth", "acoustic"]
)
entity = hypervisor.spawn(manifest)
```

---

## Dashboard Architecture

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
