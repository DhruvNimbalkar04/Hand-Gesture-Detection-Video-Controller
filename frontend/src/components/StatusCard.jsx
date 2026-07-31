function StatusCard({ gesture, hand, status }) {
    return (
        <div style={{ textAlign: "center", marginTop: "10px" }}>
            <h2>Gesture: {gesture}</h2>

            <h3>Hand: {hand}</h3>

            <h3>Status: {status}</h3>
        </div>
    );
}

export default StatusCard;