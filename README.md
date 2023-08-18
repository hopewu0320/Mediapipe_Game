>Prerequisite
>>pip install mediapipe  
>>python 3.7
# Quickstart
```python
python mediapipe_test.py
```
# Introdiction
- ### MediaPipe is a cross-platform framework, created by Google, for building multimodal applied machine learning pipelines
- ### Touch square and circle,which can get 10 and 30 points,respectively.
- ### Countdown from 30 seconds
# SubModule

## find_quadrant():  
### To check which quadrant is the circle in
```python
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
```
## circle_position():  
### Get circle position,which not show up in the same quadrant of the rectangle
```python
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
```
---
### Rectangle is in random positon, and circle not show up in the same quadrant of the rectangle
```python
if run_rectangle:
    run_rectangle= False    # 如果沒有碰到，就一直是 False ( 不會更換位置 )
    rx = random.randint(100,400)    # 隨機 x 座標
    ry = random.randint(100,300)   # 隨機 y 座標
            
            
if run_circle:
    run_circle=False
    quadrant=find_quadrant(rx,ry)
    rx_circle,ry_circle=circle_position()
```
