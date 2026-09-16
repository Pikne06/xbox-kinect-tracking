# Kinect Presence Detection Media Controller

A Windows Python application that uses a Microsoft Kinect v2 depth sensor to detect user presence and automatically toggle media playback.

## Features

- Depth-based presence detection
- Stable state changes with frame confirmation
- Automatic play/pause control using the media key
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

Presence is detected from depth pixels within 2 meters. A state change must be detected across several consecutive frames to reduce false triggers from Kinect depth noise.

The controller uses the following defaults:

- Maximum detection distance: 2 meters
- Minimum close pixels: 500
- State confirmations: 5 frames
- Poll interval: 50 ms

To adjust these values, edit the constants at the top of `pauser.py`.

The Kinect should have a clear view of the user, ideally from roughly 0.5–2.5 meters away.

The first detected state is used as the starting state, so the controller does not send a media key immediately after launch.

## Notes

The media key is a toggle rather than an absolute play/pause command. The application therefore reacts to presence changes instead of trying to determine the current state of the media player.

The project requires the Kinect v2 hardware and Windows Kinect Runtime. The sensor may stop responding after extended idle periods depending on the USB power-management configuration.
