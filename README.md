# Kinect Presence Detection Media Controller

A Python application that uses Microsoft Kinect v2 sensor to automatically pause/play media based on user presence detection using depth frame analysis.

Built with the [PyKinect2 Forked Wrapper](https://github.com/jiang131072/pykinect-2024) which enables writing Kinect applications in Python.

## Features

- **Automatic Media Control**: Pauses media when user leaves, plays when user appears
- **Depth-based Detection**: Uses Kinect depth sensor for reliable presence detection
- **Low Latency**: Responds within ~50ms to presence changes
- **State Tracking**: Prevents rapid toggling with intelligent state management

## Requirements

- **Windows 10/11**
- **Python 3.12.3**
- **Microsoft Kinect v2 Sensor** (hardware)
- **Kinect for Windows Runtime 2.2.1811** (drivers)

## Installation

### 1. Install Kinect Hardware Drivers

1. Download and install **[Python 3.12.3](https://www.python.org/downloads/release/python-3123/)**
2. Download and install **[Kinect for Windows Runtime 2.2.1811](https://www.microsoft.com/en-us/download/details.aspx?id=44561)**
   - During installation, navigate to the installation folder
   - Right-click **kinectsensor.inf** → Install

### 2. Clone and Setup Repository

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/kinectproject.git
cd kinectproject
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install comtypes
pip install -r requirements.txt
```

## Usage

```bash
python pauser.py
```

The script will:
- Display "Warming up sensor for 2 seconds..."
- Monitor depth frames continuously
- Print status when presence changes:
  - "Body appeared → Playing" - when user appears
  - "Body disappeared → Paused" - when user leaves

Press `Ctrl+C` to exit.

## Configuration

Edit `pauser.py` to adjust detection sensitivity:

```python
close_pixels = np.count_nonzero((depth_data > 0) & (depth_data < 2000))  # Distance threshold (mm)
body_detected = close_pixels > 500  # Minimum pixels threshold
```

- **`2000`**: Distance threshold in millimeters (2 meters). Increase for farther detection.
- **`500`**: Minimum pixel count required for detection. Increase for stricter detection.

## Known Issues

- Sensor may idle after ~15 seconds (hardware limitation)
- Requires Windows USB power management to be configured correctly

## Hardware Notes

- Kinect v2 uses **depth data** for detection, not RGB
- Optimal detection range: 0.5 - 2.5 meters
- Requires clear line of sight to sensor

## License

MIT

## Author

Created with PyKinect2
