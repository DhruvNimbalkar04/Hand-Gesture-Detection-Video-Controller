import cv2 as cv
import mediapipe as mp
import math
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

cam = cv.VideoCapture(0)

prevVolume = -1
prevGesture = None


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)


while True:

    success, frame = cam.read()

    if not success:
        break

    frame = cv.flip(frame, 1)

    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand_landmarks, handeness in zip(result.multi_hand_landmarks, result.multi_handedness):

            hand_type = handeness.classification[0].label

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = []
            fingers = []
            tipids = [4, 8, 12, 16, 20]

            for id, landmark in enumerate(hand_landmarks.landmark):

                h, w, c = frame.shape

                cx = int(landmark.x * w)
                cy = int(landmark.y * h)

                landmarks.append([id, cx, cy])

            if hand_type == "Right":
                fingers.append(1 if landmarks[4][1] < landmarks[3][1] else 0)
            else:
                fingers.append(1 if landmarks[4][1] > landmarks[3][1] else 0)

            for i in range(1, 5):
                if landmarks[tipids[i]][2] < landmarks[tipids[i] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            cv.putText(
                frame,
                str(fingers),
                (20, 150),
                cv.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
            )

            gesture = "unknown"
            total_fingers = sum(fingers)

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

                    volume = np.interp(
                        distance(index, thumb),
                        [15, 100],
                        [0, 100]
                    )

                    volume = round(volume / 5) * 5

                    cv.line(frame, index, thumb, (0, 255, 0), 2)

                    if volume != prevVolume:
                        print("Volume :", volume)
                        prevVolume = volume

                elif fingers == [1, 1, 1, 1, 1]:
                    gesture = "unmute"

                elif fingers == [0, 0, 0, 0, 0]:
                    gesture = "mute"

            if gesture != "unknown" and gesture != prevGesture:
                print(gesture)
                prevGesture = gesture

    cv.imshow("Hand Gesture", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()