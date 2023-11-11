"""
Install all required packages:
run 'pip install -r requirements.txt'

"""
import cv2
import numpy as np
import mediapipe as mp
from collections import deque


def exit_button_pressed():  # exit
    cap.release()
    cv2.destroyAllWindows()
    exit()


# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]


# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# The kernel to be used for dilation purpose
kernel = np.ones((5, 5), np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Here is code for Canvas setup
paintWindow = np.zeros((490, 780, 3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40, 4), (140, 40), (255, 0, 0), 2)
PaintWindow = cv2.rectangle(paintWindow, (160, 4), (260, 40), (0, 255, 0), 2)
paintWindow = cv2.rectangle(paintWindow, (280, 4), (380, 40), (0, 0, 255), 2)
paintWindow = cv2.rectangle(paintWindow, (400, 4), (500, 40), (0, 255, 255), 2)
paintWindow = cv2.rectangle(paintWindow, (520, 4), (620, 40), (0, 0, 0), 2)
paintWindow = cv2.rectangle(paintWindow, (640, 4), (740, 40), (0, 0, 0), 2)

# Adding text in boxes.. syntax( window_type, "text", location on x-y plane,font style, font scale, color code (rgb),thickness, line type)

cv2.putText(
    paintWindow,
    "BLUE",
    (70, 25),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.5,
    (0, 0, 0),
    2,
    cv2.LINE_AA,
)
cv2.putText(
    paintWindow,
    "GREEN",
    (180, 25),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.5,
    (0, 0, 0),
    2,
    cv2.LINE_AA,
)
cv2.putText(
    paintWindow,
    "RED",
    (310, 25),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.5,
    (0, 0, 0),
    2,
    cv2.LINE_AA,
)
cv2.putText(
    paintWindow,
    "YELLOW",
    (420, 25),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.5,
    (0, 0, 0),
    2,
    cv2.LINE_AA,
)
cv2.putText(
    paintWindow,
    "CLEAR",
    (545, 25),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.5,
    (0, 0, 0),
    2,
    cv2.LINE_AA,
)
cv2.putText(
    paintWindow,
    "QUIT",
    (670, 25),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.5,
    (0, 0, 0),
    2,
    cv2.LINE_AA,
)
cv2.namedWindow("Paint", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Paint", 600, 400)

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils


# Initialize the webcam
cap = cv2.VideoCapture(0)
ret = True
while ret:
    ret, frame = cap.read()
    x, y, c = frame.shape
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if not ret:
        print("Can't access camera")
        break

    frame = cv2.rectangle(frame, (30, 4), (110, 40), (255, 0, 0), 2)
    frame = cv2.rectangle(frame, (130, 4), (210, 40), (0, 255, 0), 2)
    frame = cv2.rectangle(frame, (230, 4), (310, 40), (0, 0, 255), 2)
    frame = cv2.rectangle(frame, (330, 4), (410, 40), (0, 255, 255), 2)
    frame = cv2.rectangle(frame, (430, 4), (510, 40), (0, 0, 0), 2)
    frame = cv2.rectangle(frame, (530, 4), (610, 40), (0, 0, 0), 2)
    # Adding text in boxes.. syntax( window_type, "text", location on x-y plane,font style, font scale, color code (rgb), thickness, line type)
    cv2.putText(
        frame,
        "BLUE",
        (50, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "GREEN",
        (145, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "RED",
        (255, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "YELLOW",
        (340, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "CLEAR",
        (450, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "QUIT",
        (555, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Output", 600, 400)

    result = hands.process(framergb)

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)

                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        fore_finger = (landmarks[8][0], landmarks[8][1])
        center = fore_finger
        thumb = (landmarks[4][0], landmarks[4][1])
        cv2.circle(frame, center, 3, (0, 255, 0), -1)
        print(center[1] - thumb[1])

        if thumb[1] - center[1] < 30:  # Pause drawing (joining thumb and forefinger)
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        elif center[1] <= 40:
            if 30 <= center[0] <= 110:
                colorIndex = 0  # Blue
            elif 130 <= center[0] <= 210:
                colorIndex = 1  # Green
            elif 230 <= center[0] <= 310:
                colorIndex = 2  # Red
            elif 330 <= center[0] <= 410:
                colorIndex = 3  # Yellow
            elif 430 <= center[0] <= 510:  # Clear
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[67:, :, :] = 255
            elif 530 <= center[0] <= 610:
                exit_button_pressed()  # Exit

        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw lines of all the colors on the canvas and frame
    points = [bpoints, gpoints, rpoints, ypoints]

    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(
                    paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2
                )

    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) == ord("q"):
        exit_button_pressed()
