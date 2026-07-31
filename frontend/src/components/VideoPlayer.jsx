import { useEffect, useRef, useState } from "react";

export default function VideoPlayer({ gesture, volume }) {
    const videoRef = useRef(null);
    const [videoURL, setVideoURL] = useState("");
    const [showLike, setShowLike] = useState(false);
    const lastGestureRef = useRef("");
    const lastActionTimeRef = useRef(0);

    const handleVideo = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setVideoURL(URL.createObjectURL(file));
    };

    useEffect(() => {
        if (!videoRef.current || !gesture) return;

        const video = videoRef.current;
        const now = Date.now();

        if (gesture === "play") {
            video.play().catch(() => {});
        } else if (gesture === "pause") {
            video.pause();
        } else if (gesture === "forward-10s") {
            if (
                lastGestureRef.current !== "forward-10s" ||
                now - lastActionTimeRef.current > 1200
            ) {
                video.currentTime = Math.min(
                    video.duration || 0,
                    video.currentTime + 10
                );
                lastActionTimeRef.current = now;
            }
        } else if (gesture === "backward-10s") {
            if (
                lastGestureRef.current !== "backward-10s" ||
                now - lastActionTimeRef.current > 1200
            ) {
                video.currentTime = Math.max(0, video.currentTime - 10);
                lastActionTimeRef.current = now;
            }
        } else if (gesture === "mute") {
            video.muted = true;
        } else if (gesture === "unmute") {
            video.muted = false;
        } else if (gesture === "like") {
            if (lastGestureRef.current !== "like") {
                setShowLike(true);
                setTimeout(() => setShowLike(false), 1000);
            }
        }

        lastGestureRef.current = gesture;
    }, [gesture]);

    useEffect(() => {
        if (!videoRef.current || volume === null || volume === undefined) return;
        const video = videoRef.current;
        video.volume = Math.max(0, Math.min(1, volume / 100));
        if (volume > 0) {
            video.muted = false;
        }
    }, [volume]);

    return (
        <div className="video-card">
            <div className="video-header">
                <h2>Video Player</h2>

                <label className="upload-btn">
                    Select Movie
                    <input
                        type="file"
                        accept="video/*"
                        hidden
                        onChange={handleVideo}
                    />
                </label>
            </div>

            <div className="video-body">
                {videoURL ? (
                    <>
                        <video ref={videoRef} controls className="movie-video">
                            <source src={videoURL} type="video/mp4" />
                        </video>
                    </>
                ) : (
                    <div className="empty-video">Select a movie to start</div>
                )}
            </div>
        </div>
    );
}