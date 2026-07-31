import cv2 as cv
import mediapipe as mp
import math


class HandGestureDetector:

    def __init__(self):
        self.helper_hands = mp.solutions.hands
        self.hands = self.helper_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.draw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findDistance(self, p1, p2):
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
            "frame": frame,
        }

        if result.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(
                result.multi_hand_landmarks,
                result.multi_handedness,
            ):
                hand_type = handedness.classification[0].label

                self.draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.helper_hands.HAND_CONNECTIONS,
                )

                landmarks = []
                fingers = []

                h, w, c = frame.shape

                for idx, landmark in enumerate(hand_landmarks.landmark):
                    cx = int(landmark.x * w)
                    cy = int(landmark.y * h)
                    landmarks.append([idx, cx, cy])
                    cv.circle(frame, (cx, cy), 5, (255, 0, 255), cv.FILLED)

                if hand_type == "Right":
                    fingers.append(1 if landmarks[4][1] < landmarks[3][1] else 0)
                else:
                    fingers.append(1 if landmarks[4][1] > landmarks[3][1] else 0)

                for i in range(1, 5):
                    if landmarks[self.tipIds[i]][2] < landmarks[self.tipIds[i] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = sum(fingers)
                gesture = "DONT KNOW"

                if fingers == [0, 0, 0, 0, 0]:
                    gesture = "Fist"
                elif fingers == [1, 1, 1, 1, 1]:
                    gesture = "Open Palm"
                elif fingers == [0, 1, 1, 0, 0]:
                    gesture = "Two"
                elif fingers == [0, 1, 0, 0, 0]:
                    gesture = "Pointing"
                elif fingers == [1, 0, 0, 0, 0]:
                    gesture = "Thumbs Up"
                elif fingers == [0, 0, 0, 0, 1]:
                    gesture = "Pinky"
                elif total_fingers == 5:
                    gesture = "Open Palm"
                elif total_fingers == 4:
                    gesture = "Four Fingers"
                elif total_fingers == 3:
                    gesture = "Three Fingers"
                elif total_fingers == 2:
                    gesture = "Two Fingers"
                elif total_fingers == 1:
                    gesture = "One Finger"

                thumb = (landmarks[4][1], landmarks[4][2])
                index = (landmarks[8][1], landmarks[8][2])
                dist = self.findDistance(thumb, index)

                if dist < 30 and (fingers[2] or fingers[3] or fingers[4]):
                    gesture = "OK"

                response = {
                    "gesture": gesture,
                    "hand": hand_type,
                    "status": "Detected",
                    "frame": frame,
                }

        return response