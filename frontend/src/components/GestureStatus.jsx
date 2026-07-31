export default function GestureStatus(props) {

    return (

        <div className="card">

            <h3>Gesture Status</h3>

            <div className="gesture-content">

                <h2>{props.gesture}</h2>

                <p>Hand: <span>{props.hand}</span></p>

            </div>

        </div>

    );

}