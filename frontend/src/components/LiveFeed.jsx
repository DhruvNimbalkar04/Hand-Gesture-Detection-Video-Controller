import { useEffect, useRef } from "react";
import WebCamView from "./WebCamView";
import api from "../services/api";

export default function LiveFeed({ setGesture, setHand, setVolume }) {
    const webcamRef = useRef(null);

    useEffect(() => {
        const interval = setInterval(async () => {
            if (!webcamRef.current) return;

            const image = webcamRef.current.getScreenshot();
            if (!image) return;

            try {
                const response = await api.post("detect_movie/", { image });

                if (response.data.gesture) {
                    setGesture(response.data.gesture);
                }
                if (response.data.hand) {
                    setHand(response.data.hand);
                }
                if (response.data.volume !== undefined) {
                    setVolume(response.data.volume);
                }
            } catch (error) {
                console.error(error);
            }
        }, 150);

        return () => clearInterval(interval);
    }, [setGesture, setHand, setVolume]);

    return (
        <div className="card">
            <div className="card-header">
                <h3>Live Feed</h3>
            </div>

            <div className="camera-container">
                <WebCamView ref={webcamRef} />
            </div>
        </div>
    );
}