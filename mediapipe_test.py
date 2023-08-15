import cv2
import mediapipe as mp
import random
import time

radius=30
RED=(0,0,255)
score=0
org=(30,30)
time_org = (500,30)
fontScale=1
thickness=2
font=cv2.FONT_HERSHEY_SIMPLEX
countTime = 30 #30 seconds to go

def find_quadrant(x,y):
    if x<=w and x>=w/2 and y>0 and y<h/2:
        quadrant="first"
    elif x<w/2 and x>0 and y>=0 and y<=h/2:
        quadrant="second"
    elif x<w/2 and x>0 and y>h/2 and y<h:
        quadrant="third"
    elif x<w and x>w/2 and y>h/2 and y<h:
        quadrant="fourth"
    return quadrant

def circle_position():
    if quadrant=="first":
        rx_circle=random.randint(100,w/2)
        ry_circle=random.randint(100,300)
    elif quadrant=="second":
        rx_circle=random.randint(w/2+100,w-100)
        ry_circle=random.randint(100,300)
    elif quadrant=="third":
        rx_circle=random.randint(w/2+100,w-100)
        ry_circle=random.randint(100,300)
    elif quadrant=="fourth":
        rx_circle=random.randint(100,w/2)
        ry_circle=random.randint(100,300)
    return (rx_circle,ry_circle)

mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_hands = mp.solutions.hands                    # mediapipe 偵測手掌方法

cap = cv2.VideoCapture(0)
startTime = time.time()

# mediapipe 啟用偵測手掌
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.8) as hands:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    run_rectangle= True         # 設定是否更動觸碰區位置
    run_circle=True
    while True:
        ret, img = cap.read()
        img=cv2.flip(img,1)
        if not ret:
            print("Cannot receive frame")
            break
          # 調整畫面尺寸
        size = img.shape   # 取得攝影機影像尺寸
        w = size[1]        # 取得畫面寬度
        h = size[0]        # 取得畫面高度
        
        if run_rectangle:
            run_rectangle= False    # 如果沒有碰到，就一直是 False ( 不會更換位置 )
            rx = random.randint(100,400)    # 隨機 x 座標
            ry = random.randint(100,300)   # 隨機 y 座標
            
            
        if run_circle:
            run_circle=False
            quadrant=find_quadrant(rx,ry)
            rx_circle,ry_circle=circle_position()
                
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
        results = hands.process(img2)                 # 偵測手掌
        if results.multi_hand_landmarks:  #multi_hand_landmarks回傳一個list裡面有21個點座標
            for hand_landmarks in results.multi_hand_landmarks:
                x = hand_landmarks.landmark[7].x * w   # 取得食指末端 x 座標(根據畫面長寬劃分為[0,1])
                y = hand_landmarks.landmark[7].y * h   # 取得食指末端 y 座標(同上)
                #print(x,y)
                if x>rx and x<(rx+80) and y>ry and y<(ry+80): #方形被碰到
                    run_rectangle= True
                    score+=10
                    print(score)
                if x>(rx_circle-radius) and x<(rx_circle+radius) and y>(ry_circle-radius) and y<(ry_circle+radius):
                    run_circle=True
                    score+=30
                    print(score)
                    
                # 將節點和骨架繪製到影像中
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        currentTime = time.time()
        elapsedTime = currentTime - startTime
        remainingTime = countTime - elapsedTime
        

        cv2.circle(img, (rx_circle,ry_circle), radius, RED, thickness)
        cv2.rectangle(img,(rx,ry),(rx+80,ry+80),RED,5)   # 畫出觸碰區
        text=f'Score:{score}'
        img=cv2.putText(img,text,org,font,fontScale,RED,thickness,cv2.LINE_AA)

        if remainingTime >= 0.0:
            img=cv2.putText(img,"T:{:.2f}".format(remainingTime),time_org,font,fontScale,RED,thickness,cv2.LINE_AA)
        else:
            img=cv2.putText(img,"T: End",time_org,font,fontScale,RED,thickness,cv2.LINE_AA)

        cv2.imshow('Mediapipe_Game', img)
        if cv2.waitKey(5) == ord('q'):
            break    # 按下 q 鍵停止
cap.release()
cv2.destroyAllWindows()