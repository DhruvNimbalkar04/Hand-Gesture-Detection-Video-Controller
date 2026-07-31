
export default function HelpCard() {
    return (
        <div className="help-card">
            <div className="help-title">
                <h3>Gesture Guide</h3>
            </div>
            <ul className="help-list">
                <li><strong>Left Fist:</strong> Pause</li>
                <li><strong>Left Open Palm:</strong> Play</li>
                <li><strong>Left 1 Finger:</strong> Forward 10s</li>
                <li><strong>Left 2 Fingers:</strong> Backward 10s</li>
                <li><strong>Left Thumbs Up:</strong> Like</li>
                <li><strong>Right Pinch:</strong> Control Volume</li>
                <li><strong>Right Open Palm / Fist:</strong> Unmute / Mute</li>
            </ul>
        </div>
    );
}