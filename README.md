# Spotify Road Trip Shuffle
An application for PC that allows you to shuffle a Spotify playlist by album while keeping the songs in chronological order. Think of being on a road trip and changing CD's/tapes out.

## How to Use

1. Create a Spotify App on their website
2. Replace `CLIENT_ID` and `CLIENT_SECRET` in `spotify_utils.py` with your Spotify App credentials.
3. Run `spotify_road_trip_gui.py` to launch the GUI.
4. On first use, you'll be asked to log in with your Spotify account.

## Optional

You can package this app into a single executable using PyInstaller:

```
pip install pyinstaller
pyinstaller --onefile --windowed spotify_road_trip_gui.py
```

## Current Road Map

1. Create a secure backend authorization using FastAPI so users don't need to create their own Spotify App
2. Use backend for API calls instead of the app itself
3. Build Android version
