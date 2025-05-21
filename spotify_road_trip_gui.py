import tkinter as tk
from tkinter import messagebox, font
from spotify_utils import (
    get_spotify_client,
    get_user_playlists,
    get_tracks_grouped_by_album,
    shuffle_albums,
    create_road_trip_playlist
)

def start_app():
    """
    Main function to launch the Tkinter GUI app.
    Authenticates the user, fetches playlists, lets the user pick one,
    and creates a shuffled "Road Trip Shuffle" playlist.
    """
    try:
        sp = get_spotify_client()
        user = sp.current_user()
        playlists = get_user_playlists(sp)

        user_id = user['id']

        # Separate your playlists
        your_playlists = [p for p in playlists if p['owner']['id'] == user_id]
        other_playlists = [p for p in playlists if p['owner']['id'] != user_id]

        playlist_items = []

        # Add your playlists first
        if your_playlists:
            playlist_items.append(("------ Your Playlists ------", None))
            for p in sorted(your_playlists, key=lambda x: x['name'].lower()):
                playlist_items.append((p['name'], p['id']))

        # Then group other playlists by owner
        grouped = {}
        for p in other_playlists:
            owner = p['owner']['display_name'] or "Unknown"
            grouped.setdefault(owner, []).append(p)

        for owner in sorted(grouped.keys()):
            playlist_items.append((f"------ Playlists by {owner} ------", None))
            for p in sorted(grouped[owner], key=lambda x: x['name'].lower()):
                playlist_items.append((p['name'], p['id']))


        def create_playlist():
            """
            Called when user clicks the button to create a Road Trip playlist.
            Gets the selected playlist, fetches tracks, shuffles albums,
            creates a new playlist and shows the link.
            """
            selection = playlist_listbox.curselection()
            if not selection:
                messagebox.showwarning("No playlist selected", "Please select a playlist.")
                return
            selected_name, playlist_id = playlist_items[selection[0]]
            if playlist_id is None:
                messagebox.showwarning("Invalid selection", "Please select an actual playlist.")
                return
            
            # Fetch tracks grouped by album and shuffle albums
            albums = get_tracks_grouped_by_album(sp, playlist_id)
            shuffled_tracks = shuffle_albums(albums)

            # Create new playlist and get its Spotify URL
            url = create_road_trip_playlist(sp, user['id'], selected_name, shuffled_tracks)
            messagebox.showinfo("Playlist Created", f"New playlist created:\n{url}")

        # Setup GUI
        root = tk.Tk()
        root.title("Spotify Road Trip Shuffler")
        root.geometry("450x450")
        root.configure(bg="#1DB954") # Spotify green background
        root.resizable(False, False)

        heading_font = font.Font(family="Helvetica", size=16, weight="bold")
        normal_font = font.Font(family="Helvetica", size=12)

        # Header labels
        tk.Label(root, text="🎶 Road Trip Shuffler", font=heading_font, bg="#1DB954", fg="white").pack(pady=(20, 10))
        tk.Label(root, text="Select a playlist:", font=normal_font, bg="#1DB954", fg="white").pack(pady=(0, 5))

        # # Scrollable listbox container
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        playlist_listbox = tk.Listbox(list_frame, width=50, height=15, font=normal_font, yscrollcommand=scrollbar.set)
        
        # Populate listbox with playlist names and group headers
        for name, _ in playlist_items:
            playlist_listbox.insert(tk.END, name)
        playlist_listbox.pack(side=tk.LEFT)
        scrollbar.config(command=playlist_listbox.yview)

        # Button to trigger playlist creation
        tk.Button(
            root,
            text="Create Road Trip Playlist",
            command=create_playlist,
            bg="white",
            fg="#1DB954",
            activebackground="#18ac4d",
            font=normal_font,
            width=25,
            height=2
        ).pack(pady=15)

        root.mainloop()

    except Exception as e:
        # Show any errors that occur during setup or runtime
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    start_app()
