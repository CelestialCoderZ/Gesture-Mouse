import cv2, mediapipe as mp, pyautogui, serial, time, numpy as np

# ---- CONFIG ----
SERIAL_PORT = "COM3"   # <-- Change this! e.g. COM3 on Windows, /dev/ttyUSB0 on Linux
BAUD = 115200
LEFT_THRESH = 15       # cm for left click
RIGHT_THRESH = 15      # cm for right click
# -----------------

# Screen size
sw, sh = pyautogui.size()

# Open serial
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.01)
time.sleep(1)

# Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

left_down = False
right_ready = True

def read_ultrasonic():
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        if ',' in line:
            try:
                d1, d2 = map(int, line.split(','))
                return d1, d2
            except:
                return None, None
    return None, None

while True:
    ok, frame = cap.read()
    if not ok: break
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    if res.multi_hand_landmarks:
        hand = res.multi_hand_landmarks[0]
        tip = hand.landmark[8]  # index fingertip
        x, y = int(tip.x * w), int(tip.y * h)

        draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        cv2.circle(frame, (x,y), 8, (0,255,0), -1)

        # Map to screen size
        sx = np.interp(x, [50, w-50], [0, sw])
        sy = np.interp(y, [50, h-50], [0, sh])
        pyautogui.moveTo(sx, sy)

    # Read sensors
    d1, d2 = read_ultrasonic()

    # Left click (hold)
    if d1 and d1 < LEFT_THRESH and not left_down:
        pyautogui.mouseDown()
        left_down = True
    elif d1 and d1 > LEFT_THRESH+3 and left_down:
        pyautogui.mouseUp()
        left_down = False

    # Right click (tap)
    if d2 and d2 < RIGHT_THRESH and right_ready:
        pyautogui.click(button='right')
        right_ready = False
    elif d2 and d2 > RIGHT_THRESH+3:
        right_ready = True

    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27: break

cap.release()
ser.close()
cv2.destroyAllWindows()
