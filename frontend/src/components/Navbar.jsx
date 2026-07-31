import { NavLink } from "react-router-dom";

export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-left">
                <h2>Hand Gesture Video Controller</h2>
            </div>

            <div className="navbar-right">
                <div className="nav-links">
                    <NavLink
                        to="/"
                        className={({ isActive }) =>
                            isActive ? "nav-link active" : "nav-link"
                        }
                    >
                        Home
                    </NavLink>
                    <NavLink
                        to="/movie"
                        className={({ isActive }) =>
                            isActive ? "nav-link active" : "nav-link"
                        }
                    >
                        Movie Player
                    </NavLink>
                </div>
            </div>
        </nav>
    );
}