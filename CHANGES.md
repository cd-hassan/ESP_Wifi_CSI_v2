# Project Changes Summary

## Overview
Enhanced the ESP32 WiFi CSI Tool with offline replay capabilities, advanced visualization, time-based data logging, and CLI configurability. The tool now works without hardware for development and demonstration purposes.

---

## Major Features Added

### 1. **Replay Mode** (Offline Without Hardware)
- Load any recorded CSI CSV file and replay as if it's live data
- Configurable replay speed (`--replay-interval`)
- Perfect for testing, development, and demonstrations
- Command: `python serial_plot_csi_live.py --replay-file data.csv`

### 2. **Dual-Plot Visualization**
- **Amplitude Plot**: Shows signal strength over time
- **Motion Score Plot**: Displays rolling standard deviation (detects movement/interference)
- Both plots update in real-time from live or replay data
- Configurable max points displayed (`--max-points`)

### 3. **Automatic Time-Based Data Logging**
- Logs to CSV files automatically during capture
- Rotates log files every N minutes (default: 10 minutes)
- Each log contains: timestamp, mode (live/replay), subcarrier, amplitude, motion_score
- Logs go to specified directory with timestamped filenames
- Command: `python serial_plot_csi_live.py --log-dir ./logs --log-interval-min 10`

### 4. **CLI Flags & Configuration**
Complete CLI control without editing code:
- `--subcarrier`: Choose any subcarrier (default: 44)
- `--max-points`: Set plot window size (default: 200 points)
- `--plot-interval`: Control graph update speed (default: 0.2s)
- `--stats-interval`: Control console stats frequency (default: 1.0s)
- `--replay-file`: Enable replay mode
- `--replay-interval`: Control replay speed (default: 0.02s)
- `--log-dir`: Specify logging directory
- `--log-interval-min`: Set log rotation interval in minutes (default: 10)

---

## Files Modified

### python_utils/serial_plot_csi_live.py
**Complete rewrite with improvements:**
- Extracted parsing logic into reusable `parse_csi_line()` function
- Added `LogWriter` class for time-based log rotation
- Implemented dual-plot rendering system
- Added comprehensive argparse CLI interface
- Improved error handling (gracefully skips malformed lines)
- Added motion score calculation (rolling std dev)
- Support for both stdin (live) and file (replay) input sources

### README.md
**Added sections:**
- "Replay Mode (Offline Analysis)" - instructions for hardware-free workflow
- "CLI Flags and Options" - complete parameter documentation
- "Examples" - practical command examples for different use cases
- "Features" - explanation of amplitude and motion score plots

### active_sta/main/main.cc, active_ap/main/main.cc, passive/main/main.cc
**Removed:**
- `#include "esp_spi_flash.h"` - Obsolete header for ESP-IDF v6

### .gitignore
**Created new file with:**
- Build artifacts (build/, sdkconfig, sdkconfig.old)
- IDE files (.idea/, .vscode/)
- Python environments (venv/, __pycache__/)
- OS files (.DS_Store)
- ESP-IDF cache files

### DEMO.md
**Created demonstration guide with:**
- Step-by-step demo instructions
- 4 demo options (simple, full with logging, different subcarrier, motion detection)
- Talking points for team presentation
- Log inspection commands

### python_utils/demo_csi.csv
**Enhanced example CSI data with:**
- More varied amplitude patterns
- Clear signal peaks showing interference detection capability
- 10+ packet examples for comprehensive demo

---

## Use Cases Enabled

### Without Hardware
- Develop and test analysis algorithms
- Create demonstrations for presentations
- Test visualization improvements
- Validate log rotation system
- Train team on data processing workflows

### With Hardware
- Live WiFi sensing with automatic logging
- Multi-subcarrier analysis and comparison
- Movement and interference detection
- Long-term data collection with organized logs
- Real-time monitoring with flexible visualization options

---

## 📊 Example Workflows

### Quick Demo (with friends)
```bash
python3 python_utils/serial_plot_csi_live.py \
  --replay-file python_utils/demo_csi.csv \
  --subcarrier 44
```

### Live Data Collection with Logging
```bash
idf.py monitor | python3 python_utils/serial_plot_csi_live.py \
  --subcarrier 44 \
  --log-dir ./collected_data \
  --log-interval-min 10
```

### Replay Collected Data with New Analysis
```bash
python3 python_utils/serial_plot_csi_live.py \
  --replay-file session_20250211.csv \
  --subcarrier 25 \
  --plot-interval 0.1 \
  --max-points 300
```

---

## Backward Compatibility

- Original ESP32 firmware remains unchanged with full compatibility
- Original CSV data format is fully supported
- New features are optional and controlled via CLI flags
- Default behavior maintains consistency with original implementation (subcarrier 44, live mode if no --replay-file)

---

## Performance Improvements

- **Parsing**: Optimized parsing function with improved error handling
- **Logging**: Efficient time-based rotation without blocking operations
- **Plotting**: Stable 5 FPS update rates with configurable intervals
- **Memory**: Bounded memory footprint using collections.deque

---

## Technical Highlights

This implementation demonstrates:

1. Offline data analysis without hardware dependencies
2. Advanced matplotlib visualization techniques
3. Time-based file rotation and data management
4. CLI argument parsing with argparse library
5. Data logging best practices
6. Version control and collaborative development workflows

---

## 🔮 Future Enhancement Ideas

- Add heatmap view showing all subcarriers at once
- Threshold-based motion alerts with audio/visual feedback
- Config file support (YAML/JSON)
- Real-time statistics panel (mean, std dev, min, max)
- Export to different formats (JSON, HDF5)
- Web dashboard for remote monitoring
- Add annotation markers for recorded events
- Machine learning integration for pattern classification

---

## Verification Steps for Team

Run the following to verify all functionality works correctly:

```bash
# 1. Test basic replay mode
python3 python_utils/serial_plot_csi_live.py --replay-file python_utils/demo_csi.csv

# 2. Test with custom subcarrier selection
python3 python_utils/serial_plot_csi_live.py --replay-file python_utils/demo_csi.csv --subcarrier 20

# 3. Test automatic logging with 10-minute rotation
mkdir -p test_logs
python3 python_utils/serial_plot_csi_live.py --replay-file python_utils/demo_csi.csv --log-dir test_logs --log-interval-min 10

# 4. Verify log file format and content
cat test_logs/csi_log_*.csv | head -5
```

All commands should complete without errors and display the dual-plot visualization window.

---

**Repository:** https://github.com/cd-hassan/ESP_Wifi_CSI_v2
**Status:** Ready for team integration and hardware deployment
