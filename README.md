# Spotify Road Trip Shuffle
An application for PC that allows you shuffle a Spotify playlist by album while keeping the songs in chronological order. Think of being on a road trip and changing CD's/tapes out.

An Android version is coming soon

## How to Use

1. Replace `CLIENT_ID` and `CLIENT_SECRET` in `spotify_utils.py` with your Spotify App credentials.
2. Run `spotify_road_trip_gui.py` to launch the GUI.
3. On first use, you'll be asked to log in with your Spotify account.

## Optional

You can package this app into a single executable using PyInstaller:

```
pip install pyinstaller
pyinstaller --onefile --windowed spotify_road_trip_gui.py
```
