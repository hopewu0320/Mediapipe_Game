import cv2
import mediapipe as mp
import random
import time

radius = 30
RED = (0, 0, 255)
score = 0
org = (30, 30)
time_org = (500, 30)
fontScale = 1
thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
countTime = 30  # 30 seconds to go

def find_quadrant(x, y):
    if x <= w and x >= w / 2 and y > 0 and y < h / 2:
        quadrant = "first"
    elif x < w / 2 and x > 0 and y >= 0 and y <= h / 2:
        quadrant = "second"
    elif x < w / 2 and x > 0 and y > h / 2 and y < h:
        quadrant = "third"
    elif x < w and x > w / 2 and y > h / 2 and y < h:
        quadrant = "fourth"
    return quadrant

def circle_position():
    if quadrant == "first":
        rx_circle = random.randint(100, w / 2)
        ry_circle = random.randint(100, 300)
    elif quadrant == "second":
        rx_circle = random.randint(w / 2 + 100, w - 100)
        ry_circle = random.randint(100, 300)
    elif quadrant == "third":
        rx_circle = random.randint(w / 2 + 100, w - 100)
        ry_circle = random.randint(100, 300)
    elif quadrant == "fourth":
        rx_circle = random.randint(100, w / 2)
        ry_circle = random.randint(100, 300)
    return (rx_circle, ry_circle)

mp_drawing = mp.solutions.drawing_utils  # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands  # mediapipe 偵測手掌方法

cap = cv2.VideoCapture(0)
cv2.namedWindow('Mediapipe_Game', cv2.WINDOW_NORMAL)  # 設定視窗可調整大小

def game_loop():
    global score, startTime, quadrant, rx, ry, run_rectangle, run_circle, w, h
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
                rx = random.randint(100, 400)
                ry = random.randint(100, 300)

            if run_circle:
                run_circle = False
                quadrant = find_quadrant(rx, ry)
                rx_circle, ry_circle = circle_position()

            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img2)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    x = hand_landmarks.landmark[7].x * w
                    y = hand_landmarks.landmark[7].y * h
                    if rx < x < rx + 80 and ry < y < ry + 80:
                        run_rectangle = True
                        score += 10
                        print(score)
                    if rx_circle - radius < x < rx_circle + radius and ry_circle - radius < y < ry_circle + radius:
                        run_circle = True
                        score += 30
                        print(score)
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
                cv2.waitKey(3000)  # 顯示 "T: End" 3 秒鐘
                return

            cv2.imshow('Mediapipe_Game', img)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

def main_menu():
    flash = True
    while True:
        img = cv2.imread('background.png')  # 加載您提供的圖片
        text = "Press 's' to Start"
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        thickness = 2
        text_size = cv2.getTextSize(text, font, fontScale, thickness)[0]
        text_x = (img.shape[1] - text_size[0]) // 2
        text_y = (text_size[1]) // 2 + 50  # 這裡調整文字的 y 坐標
        print(text_size,img.shape)
        if flash:
            cv2.putText(img, text, (text_x, text_y), font, fontScale, RED, thickness, cv2.LINE_AA)
            # 畫一個框框包圍文字
            cv2.rectangle(img, (text_x - 10, text_y - text_size[1] - 10), (text_x + text_size[0] + 10, text_y + 10), RED, thickness)

        flash = not flash
        cv2.imshow('Mediapipe_Game', img)
        key = cv2.waitKey(500)  # 設置閃爍間隔
        if key == ord('s'):
            game_loop()
        elif key == ord('q'):
            break

if __name__ == "__main__":
    main_menu()
    cap.release()
    cv2.destroyAllWindows()