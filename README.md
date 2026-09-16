# Kinect Presence Detection Media Controller

A Windows Python application that uses a Microsoft Kinect v2 depth sensor to detect user presence and automatically toggle media playback.

## Features

- Depth-based presence detection
- Automatic play/pause control using the media key
- ~50 ms polling interval
- Optional system-tray GUI

## Requirements

- Windows 10/11
- Python 3.12.3
- Microsoft Kinect v2
- Kinect for Windows Runtime 2.2.1811

## Setup

1. Install Python and the Kinect Runtime.
2. Clone the repository and create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the controller:

```powershell
python pauser.py
```

Or launch the GUI:

```powershell
python pauser_gui.py
```

## Detection

Presence is detected from depth pixels within 2 meters. The default threshold is 500 valid pixels.

To adjust it, change these values in `pauser.py`:

```python
(depth_data > 0) & (depth_data < 2000)
close_pixels > 500
```

The Kinect should have a clear view of the user, ideally from roughly 0.5–2.5 meters away.

## Notes

The project requires the Kinect v2 hardware and Windows Kinect Runtime. The sensor may stop responding after extended idle periods depending on the USB power-management configuration.
