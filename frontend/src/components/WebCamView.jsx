import { forwardRef } from "react";
import Webcam from "react-webcam";

const WebcamView = forwardRef((props, ref) => {
    return (
        <Webcam
            ref={ref}
            audio={false}
            mirrored
            screenshotFormat="image/jpeg"
            videoConstraints={{
                width: 1280,
                height: 720,
                facingMode: "user",
            }}
            style={{
                width: "800px",
                maxWidth: "90vw",
                aspectRatio: "16/9",
                objectFit: "cover",
                borderRadius: "12px",
                border: "2px solid #ddd",
            }}
        />
    );
});

export default WebcamView;