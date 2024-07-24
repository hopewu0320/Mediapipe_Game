import cv2
import mediapipe as mp
import random
import time
import math

radius = 30
RED = (0, 0, 255)
score = 0
org = (30, 30)
time_org = (500, 30)
fontScale = 1
thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
countTime = 300  # 30 seconds to go

First_Generate  = True

def find_quadrant(x, y):
    if x >= w / 2 and y < h / 2:
        quadrant = "first"
    elif x < w / 2 and y < h / 2:
        quadrant = "second"
    elif x < w / 2 and y >= h / 2:
        quadrant = "third"
    elif x >= w / 2 and y >= h / 2:
        quadrant = "fourth"
    return quadrant

def generate_rectangle_position():
    global First_Generate, Circle_quadrant

    if First_Generate:
        First_Generate = False
        Rec_quadrant = random.choice(["first", "second", "third", "fourth"])
    else:
        if Circle_quadrant == "first":
            Rec_quadrant = random.choice(["second", "third", "fourth"])
        elif Circle_quadrant == "second":
            Rec_quadrant = random.choice(["first", "third", "fourth"])
        elif Circle_quadrant == "third":
            Rec_quadrant = random.choice(["first", "second", "fourth"])
        else:  # Circle_quadrant == "fourth"
            Rec_quadrant = random.choice(["first", "second", "third"])

    if Rec_quadrant == "first":
        rx = random.randint(w // 2, w - 80)
        ry = random.randint(0, h // 2 - 80)
    elif Rec_quadrant == "second":
        rx = random.randint(0, w // 2 - 80)
        ry = random.randint(0, h // 2 - 80)
    elif Rec_quadrant == "third":
        rx = random.randint(0, w // 2 - 80)
        ry = random.randint(h // 2, h - 80)
    elif Rec_quadrant == "fourth":
        rx = random.randint(w // 2, w - 80)
        ry = random.randint(h // 2, h - 80)
    return rx, ry, Rec_quadrant

def circle_position(rx, ry, Rec_quadrant):
    global Circle_quadrant
    while True:
        if Rec_quadrant == "first":
            Circle_quadrant = random.choice(["second", "third", "fourth"])
        elif Rec_quadrant == "second":
            Circle_quadrant = random.choice(["first", "third", "fourth"])
        elif Rec_quadrant == "third":
            Circle_quadrant = random.choice(["first", "second", "fourth"])
        else:  # Rec_quadrant == "fourth"
            Circle_quadrant = random.choice(["first", "second", "third"])

        if Circle_quadrant == "first":
            rx_circle = random.randint(w // 2 + radius, w - radius)
            ry_circle = random.randint(radius, h // 2 - radius)
        elif Circle_quadrant == "second":
            rx_circle = random.randint(radius, w // 2 - radius)
            ry_circle = random.randint(radius, h // 2 - radius)
        elif Circle_quadrant == "third":
            rx_circle = random.randint(radius, w // 2 - radius)
            ry_circle = random.randint(h // 2 + radius, h - radius)
        else:  # Circle_quadrant == "fourth"
            rx_circle = random.randint(w // 2 + radius, w - radius)
            ry_circle = random.randint(h // 2 + radius, h - radius)

        if not check_overlap(rx, ry, rx_circle, ry_circle):
            break
    return rx_circle, ry_circle

def check_overlap(rx, ry, rx_circle, ry_circle):
    square_center_x = rx + 40
    square_center_y = ry + 40
    distance = math.sqrt((square_center_x - rx_circle) ** 2 + (square_center_y - ry_circle) ** 2)
    if distance < radius + 40:
        return True
    return False

def countdown():
    for i in range(3, 0, -1):
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        if not ret:
            print("Cannot receive frame")
            break
        size = img.shape
        w = size[1]
        h = size[0]
        text = str(i)
        text_size = cv2.getTextSize(text, font, 5, thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = (h + text_size[1]) // 2
        img = cv2.putText(img, text, (text_x, text_y), font, 5, RED, thickness, cv2.LINE_AA)
        cv2.imshow('Mediapipe_Game', img)
        cv2.waitKey(1000)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cv2.namedWindow('Mediapipe_Game', cv2.WINDOW_NORMAL)

def game_loop():
    global score, startTime, rx, ry, run_rectangle, run_circle, w, h, Circle_quadrant
    score = 0
    startTime = time.time()

    with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.8) as hands:

        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        run_rectangle = True
        run_circle = True
        while True:
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            if not ret:
                print("Cannot receive frame")
                break
            size = img.shape
            w = size[1]
            h = size[0]

            if run_rectangle:
                run_rectangle = False
                rx, ry, Rec_quadrant = generate_rectangle_position()

            if run_circle:
                run_circle = False
                rx_circle, ry_circle = circle_position(rx, ry, Rec_quadrant)

            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img2)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    x = hand_landmarks.landmark[7].x * w
                    y = hand_landmarks.landmark[7].y * h
                    if rx < x < rx + 80 and ry < y < ry + 80:
                        run_rectangle = True
                        score += 10
                        print(f"Now Score:{score}")
                    if rx_circle - radius < x < rx_circle + radius and ry_circle - radius < y < ry_circle + radius:
                        run_circle = True
                        score += 30
                        print(f"Now Score:{score}")
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            currentTime = time.time()
            elapsedTime = currentTime - startTime
            remainingTime = countTime - elapsedTime

            cv2.circle(img, (rx_circle, ry_circle), radius, RED, thickness)
            cv2.rectangle(img, (rx, ry), (rx + 80, ry + 80), RED, 5)
            text = f'Score:{score}'
            img = cv2.putText(img, text, org, font, fontScale, RED, thickness, cv2.LINE_AA)

            if remainingTime >= 0.0:
                img = cv2.putText(img, "T:{:.2f}".format(remainingTime), time_org, font, fontScale, RED, thickness, cv2.LINE_AA)
            else:
                img = cv2.putText(img, "T: End", time_org, font, fontScale, RED, thickness, cv2.LINE_AA)
                cv2.imshow('Mediapipe_Game', img)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break
                cv2.waitKey(3000)
                return

            cv2.imshow('Mediapipe_Game', img)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

def main_menu():
    flash = True
    while True:
        img = cv2.imread('background.png')
        text = "Press 's' to Start"
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        thickness = 2
        text_size = cv2.getTextSize(text, font, fontScale, thickness)[0]
        text_x = (img.shape[1] - text_size[0]) // 2
        text_y = (text_size[1]) // 2 + 50
        if flash:
            cv2.putText(img, text, (text_x, text_y), font, fontScale, RED, thickness, cv2.LINE_AA)
            cv2.rectangle(img, (text_x - 10, text_y - text_size[1] - 10), (text_x + text_size[0] + 10, text_y + 10), RED, thickness)

        flash = not flash
        cv2.imshow('Mediapipe_Game', img)
        key = cv2.waitKey(500)
        if key == ord('s'):
            countdown()
            game_loop()
        elif key == ord('q'):
            break

if __name__ == "__main__":
    main_menu()
    cap.release()
    cv2.destroyAllWindows()
