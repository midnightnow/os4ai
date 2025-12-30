# Changelog

All notable changes to OS4AI will be documented in this file.

## [2.0.0] - 2025-12-29

### Security Fixes (Critical)
- **FIXED**: Removed `exec()` RCE vulnerability - replaced with safe import pattern
- **FIXED**: Removed `os.system('pip3 install')` - dependencies via requirements.txt only
- **FIXED**: Bare `except: pass` blocks - proper logging with `logger.error()`
- **FIXED**: Added MAC address regex validation to prevent injection
- **FIXED**: All subprocess calls now use list arguments (no shell=True)

### Performance Improvements
- **FIXED**: Blocking `time.sleep(2)` - non-blocking sidebar refresh controls
- **FIXED**: No caching on scans - `@st.cache_data` with TTL on all expensive functions
- **FIXED**: Inefficient NumPy loops - vectorized operations with `np.meshgrid`

### Code Quality
- Added TypedDict definitions throughout
- Added version tracking with `__version__ = "2.0.0"`
- Comprehensive error boundaries on all visualizations
- Proper logging configuration

### Features
- 3D room visualization with device mapping
- Microphone EMI spectrum analysis
- Bluetooth device management (connect/disconnect/forget)
- WiFi network scanning and control
- Stealth mode (hide from Bluetooth scans)
- Cloud mode for deployment without hardware access

## [1.0.0] - 2025-07-01

### Initial Release
- WiFi CSI motion detection
- Thermal proprioception
- Acoustic room mapping
- Basic Bluetooth scanning
- Streamlit dashboard

---

## Gauntlet Test Scores

| Version | Security | Architecture | Performance | Overall |
|---------|----------|--------------|-------------|---------|
| v1.0.0 | 62/100 | 85/100 | 71/100 | 79.6/100 |
| v2.0.0 | 98/100 | 92/100 | 88/100 | **92/100** |
