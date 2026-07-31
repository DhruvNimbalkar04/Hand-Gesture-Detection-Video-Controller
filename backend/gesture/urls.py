from django.urls import path
from .views import health_check, detect_gesture, detect_movie_gesture

urlpatterns = [
    path("health/", health_check),
    path("detect/", detect_gesture),
    path("detect_movie/", detect_movie_gesture),
]