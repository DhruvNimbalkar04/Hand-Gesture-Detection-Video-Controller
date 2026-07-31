import LiveFeed from "./LiveFeed";
import GestureStatus from "./GestureStatus";
import HelpCard from "./HelpCard";

export default function Sidebar({
    gesture,
    hand,
    setGesture,
    setHand,
    setVolume
}) {
    return (
        <div className="left-panel">
            <LiveFeed
                setGesture={setGesture}
                setHand={setHand}
                setVolume={setVolume}
            />

            <GestureStatus
                gesture={gesture}
                hand={hand}
            />

            <HelpCard />
        </div>
    );
}