import cv2 as cv
import mediapipe as mp
import math
import numpy as np


class MovieGestureDetector:

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tipids = [4, 8, 12, 16, 20]

    def distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.hypot(x2 - x1, y2 - y1)

    def process(self, frame):
        frame = cv.flip(frame, 1)
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        response = {
            "gesture": "No Hand",
            "hand": "",
            "status": "No Hand Detected",
            "volume": None,
            "frame": frame,
        }

        if result.multi_hand_landmarks:

            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):

                hand_type = handedness.classification[0].label

                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )

                landmarks = []
                fingers = []

                h, w, c = frame.shape
                for id, landmark in enumerate(hand_landmarks.landmark):
                    cx = int(landmark.x * w)
                    cy = int(landmark.y * h)
                    landmarks.append([id, cx, cy])


                if hand_type == "Right":
                    fingers.append(1 if landmarks[4][1] < landmarks[3][1] else 0)
                else:
                    fingers.append(1 if landmarks[4][1] > landmarks[3][1] else 0)

                for i in range(1, 5):
                    if landmarks[self.tipids[i]][2] < landmarks[self.tipids[i] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = sum(fingers)
                gesture = "unknown"
                volume = None

                if hand_type == "Right":
                    if total_fingers == 0:
                        gesture = "pause"
                    elif total_fingers == 5:
                        gesture = "play"
                    elif fingers == [0, 1, 0, 0, 0] or (total_fingers == 1 and fingers[1] == 1):
                        gesture = "forward-10s"
                    elif fingers == [0, 1, 1, 0, 0] or (total_fingers == 2 and fingers[1] == 1 and fingers[2] == 1):
                        gesture = "backward-10s"
                    elif fingers == [1, 0, 0, 0, 0] or (total_fingers == 1 and fingers[0] == 1):
                        gesture = "like"

                elif hand_type == "Left":
                    if fingers == [1, 1, 0, 0, 0]:
                        index = (landmarks[8][1], landmarks[8][2])
                        thumb = (landmarks[4][1], landmarks[4][2])
                        dist = self.distance(index, thumb)
                        vol_val = np.interp(dist, [15, 100], [0, 100])
                        volume = int(round(vol_val / 5) * 5)
                        gesture = "volume"
                    elif total_fingers == 5:
                        gesture = "unmute"
                    elif total_fingers == 0:
                        gesture = "mute"

                response = {
                    "gesture": gesture,
                    "hand": hand_type,
                    "status": "Detected",
                    "volume": volume,
                    "frame": frame,
                }

        return response