# Demo Instructions - WiFi CSI Tool with Replay Mode

When an ESP32 device is not available, the replay mode enables offline demonstration and analysis of CSI data without hardware.

## Prerequisites

Install Python dependencies:
```bash
pip install numpy matplotlib
```

## Demo Step-by-Step

### Option 1: Simple Amplitude Plot (Fastest Demo - 30 seconds)

```bash
cd /home/kali/Desktop/ESPWifiCSI/ESP32-CSI-Tool
python3 python_utils/serial_plot_csi_live.py \
  --replay-file python_utils/demo_csi.csv \
  --subcarrier 44 \
  --replay-interval 0.02
```

**Visualization Output:**

**Top Plot (Signal Amplitude by Subcarrier):**
- **Packets 1-5**: Low stable amplitude indicates weak signal or distant source.
- **Packets 6-10**: High amplitude indicates strong signal or proximity to AP.
- **Packets 11-15**: Jagged amplitude patterns indicate signal obstruction or interference.
- **Packets 16-20**: High stable amplitude resumes when obstruction clears.
- **Packets 21-24**: Amplitude decreases as signal source moves away.

**Bottom Plot (Motion Score - Rolling Standard Deviation):**
- **Flat baseline**: Indicates stable signal with minimal variation.
- **Upward spikes**: Indicates movement or interference in the signal path.
- **Transient spikes**: Brief disturbances that resolve quickly.
- **Sustained elevation**: Indicates ongoing movement in the environment.

The two plots together demonstrate how WiFi CSI can be used for motion detection and environmental analysis. Signal amplitude changes correspond to physical movement and obstruction patterns. 

### Option 2: Full Demo with Data Logging (5 minutes)

```bash
mkdir -p ~/csi_demo_logs
python3 python_utils/serial_plot_csi_live.py \
  --replay-file python_utils/demo_csi.csv \
  --subcarrier 44 \
  --log-dir ~/csi_demo_logs \
  --log-interval-min 10 \
  --replay-interval 0.02
```

**Behavior:**
- Displays the same visualization as Option 1.
- Automatically logs data to CSV files in `~/csi_demo_logs/`.
- Log files rotate every 10 minutes automatically.
- Each log entry contains: timestamp, mode (live/replay), subcarrier index, amplitude, and motion score.

**Show the logs:**
```bash
ls -lah ~/csi_demo_logs/
cat ~/csi_demo_logs/csi_log_*.csv | head -20
```

The motion_score column reveals the detection pattern: elevated values correspond to movement, while low values indicate stable conditions. This demonstrates the feasibility of using WiFi CSI for motion sensing applications.

### Option 3: Different Subcarrier Demo

```bash
python3 python_utils/serial_plot_csi_live.py \
  --replay-file python_utils/example_csi.csv \
  --subcarrier 30 \
  --replay-interval 0.02
```

Try different subcarriers: 10, 20, 30, 40, 44, 50, etc. to show different signal patterns.

### Option 4: Motion Detection Feature

```bash
python3 python_utils/serial_plot_csi_live.py \
  --replay-file python_utils/example_csi.csv \
  --subcarrier 44 \
  --replay-interval 0.02
```

**Look at the second plot (Motion Score):**
- Shows rolling standard deviation
- Spikes indicate movement or interference
- Use this to detect when something changed in the environment

## Key Capabilities Demonstrated

The replay mode demonstrates the following capabilities without requiring hardware:

1. **Real-time signal visualization** from recorded CSI data.
2. **Motion and interference detection** through signal variation analysis.
3. **Automatic data logging** with configurable rotation intervals.
4. **Multi-subcarrier analysis** with independent signal examination.
5. **Pattern analysis** of WiFi signal behavior over time.

These capabilities support various WiFi sensing applications:
- Device-free localization
- Gesture and activity recognition
- Intrusion detection
- Occupancy monitoring

## Graph Interpretation

### **Amplitude Plot (Top)**
Represents the signal strength magnitude at the selected subcarrier index.
- **High/stable values**: Strong signal propagation with minimal obstruction.
- **Low/stable values**: Weak signal propagation or significant path loss.
- **Rapidly varying/jagged values**: Signal obstruction, multipath interference, or movement-induced disruption.

### **Motion Score Plot (Bottom)**
Represents the rolling standard deviation of signal amplitude, indicating signal variability.
- **Low/flat baseline**: Stable signal conditions with minimal environmental change.
- **Upward spikes**: Rapid signal variation indicating movement or environmental disturbance.
- **Transient peaks**: Brief disruptions in the signal path that resolve quickly.
- **Sustained elevation**: Persistent signal variability indicating ongoing activity or movement.

## Narrative Analysis

The demo data presents a coherent narrative of environmental change:

1. **Packets 1-5**: Low amplitude with stable motion score indicates a distant or obstructed source.
2. **Packets 6-10**: Amplitude increases to high levels, indicating the source has moved closer or obstructions have cleared.
3. **Packets 11-15**: Amplitude becomes highly variable with elevated motion score, indicating movement or interference in the signal path.
4. **Packets 16-20**: Amplitude stabilizes at high levels, indicating movement has ceased and conditions are stable.
5. **Packets 21-24**: Amplitude decreases, indicating the source is moving away or signal strength is degrading.

This sequence demonstrates the core concept of WiFi-based sensing: extracting behavioral and environmental information purely from signal propagation characteristics.

## Stopping the Demo

Press `Ctrl+C` in the terminal to terminate execution.

## Log Files Inspection

After running Option 2, view the generated logs:
```bash
ls -lah ~/csi_demo_logs/
cat ~/csi_demo_logs/csi_log_*.csv | head -20
```

This shows the automated data collection in action.
