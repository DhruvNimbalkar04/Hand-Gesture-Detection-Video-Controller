import cv2 as cv
import mediapipe as mp
import math
import random


def findDistance(p1, p2):

    x1, y1 = p1
    x2, y2 = p2

    return math.hypot(x2 - x1, y2 - y1)



helper_hands = mp.solutions.hands
hands = helper_hands.Hands()

draw = mp.solutions.drawing_utils

cam = cv.VideoCapture(0)

while True:
    success , frame = cam.read()

    if not success:
        break

    frame = cv.flip(frame,1)

    rgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    result = hands.process(rgb)

    tipIds = [4, 8, 12, 16, 20]

    if result.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            
            hand_type = handedness.classification[0].label

            draw.draw_landmarks(
                frame,
                hand_landmarks,
                helper_hands.HAND_CONNECTIONS
            )

            landmarks = []
            fingers = []

            for id,landmark in enumerate(hand_landmarks.landmark):

                h , w , c = frame.shape
                cx = int(landmark.x * w)
                cy = int(landmark.y * h)

                landmarks.append([id, cx, cy])

                cv.circle(frame, (cx, cy), 5, (255, 0, 255), cv.FILLED)

                cv.putText(
                frame,
                str(id),                  
                (cx + 5, cy - 5),
                cv.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
                )

            if hand_type == "Right":
                if landmarks[4][1] < landmarks[3][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if landmarks[4][1] < landmarks[3][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            for i in range(1,5):
                if landmarks[tipIds[i]][2] < landmarks[tipIds[i]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)


            gesture ="DONT KNOW"
            if fingers == [0,0,0,0,0]:
                gesture = "Fist"

            elif fingers == [1,1,1,1,1]:
                gesture = "Open Palm"

            elif fingers == [0,1,1,0,0]:
                gesture = "Two"

            elif fingers == [0,1,0,0,0]:
                gesture = random.choice(["Pointing","One"])
            
            elif fingers == [1, 0, 0, 0, 0]:
                gesture = "Thumbs Up"
            
            elif fingers == [0,0,0,0,1]:
                gesture = "Pinky"

            elif fingers == [0,1,1,1,0]:
                gesture = "Three Fingers"

            elif fingers == [0,1,1,1,1]:
                gesture = "Four Fingers"
            
            thumb = (landmarks[4][1], landmarks[4][2])
            index = (landmarks[8][1], landmarks[8][2])

            distance = findDistance(thumb, index)
            if distance < 30 and (fingers[2] or fingers[3] or fingers[4]) == 1:
                gesture = "OK"

            cv.rectangle(frame, (0, 0), (640, 80), (32,42,25), -1)
            
            cv.putText(
                frame,
                str(fingers),
                (10, 150) if hand_type == "Left" else (400, 150),
                cv.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )
        

            cv.putText(
                frame,
                gesture,
                (20, 50) if hand_type == "Left" else (400, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv.putText(
                frame,
                hand_type,
                (20, 100) if hand_type == "Left" else (400, 100),
                cv.FONT_HERSHEY_COMPLEX,
                1,
                (55,23,23),
                2
            )


    cv.imshow("Hand Gesture Detection",frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break



cam.release()
cv.destroyAllWindows()