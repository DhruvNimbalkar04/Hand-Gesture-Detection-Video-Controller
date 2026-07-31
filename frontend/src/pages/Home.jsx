import { useEffect, useRef, useState } from "react";
import WebcamView from "../components/WebCamView";
import StatusCard from "../components/StatusCard";
import Navbar from "../components/Navbar";
import api from "../services/api";

function Home() {
    const webcamRef = useRef(null);

    const [gesture, setGesture] = useState("Waiting...");
    const [hand, setHand] = useState("--");
    const [status, setStatus] = useState("Camera Ready");

    useEffect(() => {
        const interval = setInterval(async () => {
            if (!webcamRef.current) return;

            const image = webcamRef.current.getScreenshot();
            if (!image) return;

            try {
                const response = await api.post("detect/", { image });
                setGesture(response.data.gesture);
                setHand(response.data.hand);
                setStatus(response.data.status);
            } catch (error) {
                console.error(error);
            }
        }, 150);

        return () => clearInterval(interval);
    }, []);

    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                minHeight: "100vh",
                paddingTop: "20px",
                background: "#f5f5f5",
            }}
        >   
            <Navbar />

            <h1>Hand Gesture Detection</h1>

            <WebcamView ref={webcamRef} />

            <StatusCard
                gesture={gesture}
                hand={hand}
                status={status}
            />
        </div>
    );
}

export default Home;