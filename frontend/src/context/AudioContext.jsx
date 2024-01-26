import { createContext, useEffect, useState } from "react";

import APIKit from "../components/spotify.js";

export const AudioContext = createContext({
  assignTrack: "",
  setAssignTrack: () => {},
  setPlaylists: () => {},
  playlists: null,
});

export default function AudioContextProvider({ children }) {
  const [assignTrack, setAssignTrack] = useState("");
  const [playlists, setPlaylists] = useState(null);

  useEffect(() => {
    fetchPlaylists();
  }, []);

  const fetchPlaylists = async () => {
    try {
      const response = await APIKit.get("me/playlists");

      const playlists = response.data.items;
      const promises = playlists.map((playlist) =>
        APIKit.get(playlist.tracks.href).then((response) => {
          playlist.tracks.items = response.data.items;
          return playlist;
        }),
      );
      const playlistsWithTracks = await Promise.all(promises);
      setPlaylists(playlistsWithTracks);
    } catch (error) {
      console.error("Error fetching playlists or tracks:", error);
    }
  };

  const value = {
    assignTrack,
    setAssignTrack,
    playlists,
    setPlaylists,
  };

  return (
    <AudioContext.Provider value={value}>{children}</AudioContext.Provider>
  );
}