import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import streamlit as st
from PIL import Image

# Initialization
st.title("GestureArtFlow")
st.sidebar.title("Controls")
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Giving different arrays to handle color points of different colors
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0
paintWindow = np.ones((490, 780, 3), np.uint8) * 255
cap = cv2.VideoCapture(0)  #Set up webcam

def draw_on_canvas(paintWindow, points):
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

while True:
    ret, frame = cap.read()
    if not ret:
        st.error("Can't access camera")
        break

    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)

    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * 780)  # Adjust the scaling based on your window size
                lmy = int(lm.y * 490)
                landmarks.append([lmx, lmy])
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

        center = (landmarks[8][0], landmarks[8][1])  # Index finger tip
        thumb = (landmarks[4][0], landmarks[4][1])   # Thumb tip

        if thumb[1] - center[1] < 30:  # Pause drawing
            bpoints.append(deque(maxlen=512))
            gpoints.append(deque(maxlen=512))
            rpoints.append(deque(maxlen=512))
            ypoints.append(deque(maxlen=512))
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
                paintWindow[:] = 255

        else:
            if colorIndex == 0:
                bpoints[-1].appendleft(center)
            elif colorIndex == 1:
                gpoints[-1].appendleft(center)
            elif colorIndex == 2:
                rpoints[-1].appendleft(center)
            elif colorIndex == 3:
                ypoints[-1].appendleft(center)

    points = [bpoints, gpoints, rpoints, ypoints]
    draw_on_canvas(paintWindow, points)

    img_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_paint = cv2.cvtColor(paintWindow, cv2.COLOR_BGR2RGB)

    st.image(img_frame, caption='Webcam Feed', use_column_width=True)
    st.image(img_paint, caption='Drawing Canvas', use_column_width=True)

    if st.button("Exit"):
        cap.release()
        break

cap.release()
