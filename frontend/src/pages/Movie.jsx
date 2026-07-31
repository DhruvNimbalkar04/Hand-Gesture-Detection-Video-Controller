import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import VideoPlayer from "../components/VideoPlayer";
import "../App.css";

export default function Movie() {
    const [gesture, setGesture] = useState("Waiting...");
    const [hand, setHand] = useState("None");
    const [volume, setVolume] = useState(null);

    return (
        <div className="movie-page">
            <Navbar />

            <div className="movie-container">
                <Sidebar
                    gesture={gesture}
                    hand={hand}
                    setGesture={setGesture}
                    setHand={setHand}
                    setVolume={setVolume}
                />

                <div className="right-panel">
                    <VideoPlayer
                        gesture={gesture}
                        volume={volume}
                    />
                </div>
            </div>

        </div>
    );
}