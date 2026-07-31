from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
import cv2 as cv
from .detector import HandGestureDetector
from .movie_detector import MovieGestureDetector
import numpy as np

detector = HandGestureDetector()
movie_detector = MovieGestureDetector()


@api_view(["GET"])
def health_check(request):
    return Response({"status": "success", "message": "Backend is running."})


@api_view(["POST"])
def detect_gesture(request):
    image_data = request.data.get("image")

    if not image_data:
        return Response({"error": "No image received"}, status=400)

    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    np_array = np.frombuffer(image_bytes, np.uint8)
    frame = cv.imdecode(np_array, cv.IMREAD_COLOR)

    result = detector.process(frame)

    return Response(
        {
            "gesture": result["gesture"],
            "hand": result["hand"],
            "status": result["status"],
        }
    )


@api_view(["POST"])
def detect_movie_gesture(request):
    image_data = request.data.get("image")

    if not image_data:
        return Response({"error": "No image received"}, status=400)

    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    np_array = np.frombuffer(image_bytes, np.uint8)
    frame = cv.imdecode(np_array, cv.IMREAD_COLOR)

    result = movie_detector.process(frame)

    return Response(
        {
            "gesture": result["gesture"],
            "hand": result["hand"],
            "status": result["status"],
            "volume": result.get("volume", None),
        }
    )