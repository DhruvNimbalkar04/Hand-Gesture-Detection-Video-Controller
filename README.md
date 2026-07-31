# Hand Gesture Video Controller

A real time computer vision-based web application that enables users to control video playback using hand gestures captured through a webcam. The system uses MediaPipe for hand landmark detection and React for an interactive user interface, providing a touchless media control experience.

# Domain Chosen

**Hand Gesture Detection**

# Why this domain?

Hand gesture recognition enables touchless Human-Computer Interaction and has applications in smart TVs, healthcare, smart homes, accessibility systems, and interactive displays. This project demonstrates the integration of computer vision, REST APIs, and modern web technologies.


# Home Page (`/`)
Recognizes common hand gestures in real time:

- Fist
- Open Palm
- Pointing
- Two Fingers
- Thumbs Up
- Pinky
- OK Gesture

# Movie Controller (`/movie`)

Gesture                                                             Action

Right Open Palm                                                     Play Video
Right Fist                                                          Pause Video
Right Pointing                                                      Forward 10 Seconds
Right Two Fingers                                                   Backward 10 Seconds
Right Thumbs Up                                                     Like
Left Thumb & Index Pinch                                            Volume Control
Left Open Palm                                                      Unmute
Left Fist                                                           Mute

- Real-time webcam processing
- Dynamic volume control
- Responsive React interface
- Low-latency gesture detection (~150 ms)


# Technology Stack
# Backend
- Python
- Django
- Django REST Framework
- OpenCV
- MediaPipe
- NumPy

# Frontend
- React
- Vite
- React Router
- React Webcam
- Axios
- React Icons
- CSS
- Javascript
- Html


## Setup & Installation

### Prerequisites

- Python 
- Node.js
- npm
- Webcam

### Backend

```bash
cd backend

python -m venv env

# Windows
env\Scripts\activate

# Linux/macOS
source env/bin/activate

pip install -r requirements.txt

python manage.py runserver
```

Backend runs at: http://127.0.0.1:8000/

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at: http://localhost:5173/


# How to Use

1. Start the backend server.
2. Start the React frontend.
3. Open `http://localhost:5173`.
4. Visit the **Home** page to test gesture recognition.
5. Visit the **Movie** page, upload an MP4 video, and control playback using hand gestures.


## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/health/` | Health Check |
| POST | `/api/detect/` | General Gesture Detection |
| POST | `/api/detect_movie/` | Movie Gesture Detection |


## Known Limitations

- Performance depends on lighting conditions.
- Supports only one user at a time.
- Recognizes predefined static gestures only.


## Future Improvements

- Custom gesture mapping
- Improved gesture accuracy
- more new features