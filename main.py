import cv2
import mediapipe as mp
import pyautogui
from pynput.mouse import Controller as MouseController
import keyboard
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import math

pyautogui.FAILSAFE = False

prev_index_finger_y = None
prev_index_finger_x = None
vel = 0
all_vel = 0
mouse_x = 0
mouse_y = 0
is_left_click = False
is_right_click = False
delta_x = 0
delta_y = 0
mouse = MouseController()

def is_key_pressed(key):
    return keyboard.is_pressed(key)

def scroll_left():
    pyautogui.scroll(-1)

def scroll_right():
    pyautogui.scroll(1)

def scroll_page_up():
    pyautogui.scroll(100)

def scroll_page_down():
    pyautogui.scroll(-100)

def move_mouse(x, y):
    pyautogui.moveTo(x, y)

def left_click():
    pyautogui.leftClick()

def right_click():
    pyautogui.rightClick()

def left_down():
    pyautogui.mouseDown()

def left_up():
    pyautogui.mouseUp()

def previous_tab():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.press('left')
    pyautogui.press('left')
    pyautogui.keyUp('alt')

def next_tab():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()

font = ImageFont.truetype("simhei.ttf", 30)
font2 = ImageFont.truetype("arialbd.ttf", 30)
font3 = ImageFont.truetype("simhei.ttf", 17)

def draw_rounded_rectangle(image, rectangle, radius, fill, outline, width):
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    if len(fill) == 3:
        fill = fill + (50,)

    draw.rounded_rectangle(rectangle, radius=radius, fill=fill, outline=outline, width=width)
    return np.array(pil_image)

def draw_text(image, text, position, font, color=(0, 255, 0)):
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    draw.text(position, text, font=font, fill=color)
    return np.array(pil_image)

def draw_tech_circle(image, center, radius):
    cv2.circle(image, center, radius, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.circle(image, center, radius - 5, (255, 0, 255), 2, cv2.LINE_AA)
    for angle in range(0, 360, 45):
        x = int(center[0] + radius * np.cos(np.radians(angle)))
        y = int(center[1] + radius * np.sin(np.radians(angle)))
        cv2.line(image, center, (x, y), (255, 255, 255), 1, cv2.LINE_AA)

def draw_circulating_arcs(image, center, radius, color=(0, 255, 0), thickness=1, angle1=0, angle2=0):
    start_angle1 = angle1
    end_angle1 = angle1 + 180
    cv2.ellipse(image, center, (radius, radius), 0, start_angle1, end_angle1, color, thickness, cv2.LINE_AA)
    start_angle2 = angle2
    end_angle2 = angle2 + 180
    cv2.ellipse(image, center, (radius + 10, radius + 10), 0, start_angle2, end_angle2, color, thickness, cv2.LINE_AA)


angle1 = 0
angle2 = 0
angle_increment = 5

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        rectangle = (10, 10, 150, 60)
        radius = 20
        fill = (0, 0, 0, 50)
        outline = (0, 192, 255)
        width = 4

        image = draw_rounded_rectangle(image, rectangle, radius, fill, outline, width)

        outline = (65, 41, 255)
        width = 2

        rectangle2 = (170, 10, 600, 60)
        image = draw_rounded_rectangle(image, rectangle2, radius, fill, outline, width)

        rectangle3 = (10, 310, 100, 400)
        image = draw_rounded_rectangle(image, rectangle3, radius, fill, outline, width)

        rect3_center_x = (rectangle3[0] + rectangle3[2]) // 2
        rect3_center_y = (rectangle3[1] + rectangle3[3]) // 2

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]

                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
                index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

                middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                middle_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
                middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
               
                ring_finger = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                
                pinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

                # Get the coordinates of hand center
                hand_center = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

                # Calculate the distance between index finger and thumb
                index_middle_distance = abs(index_finger.x - middle_finger.x) + abs(index_finger.y - middle_finger.y)
                middle_ring_distance = abs(ring_finger.x - middle_finger.x) + abs(ring_finger.y - middle_finger.y)
                index_finger_is_straight = bool((index_finger.y / index_finger_dip.y / (index_finger_dip.y / index_finger_mcp.y)) > 0)
                all_fingers_raised = bool(index_finger.y < index_finger_mcp.y and middle_finger.y < middle_finger_mcp.y and ring_finger.y < ring_finger_mcp.y and pinky.y < pinky_mcp.y)

                # Draw circulating arcs around the index finger
                index_finger_pos = (int(index_finger.x * image.shape[1]), int(index_finger.y * image.shape[0]))
                

                if prev_index_finger_y is not None:
                    delta_y = index_finger.y - prev_index_finger_y
                else:
                    delta_y = 0

                vel = vel * 0.9
                mouse.scroll(0, vel)
                prev_index_finger_y = index_finger.y

                if prev_index_finger_x is not None:
                    delta_x = index_finger.x - prev_index_finger_x
                else:
                    delta_x = 0

                prev_index_finger_x = index_finger.x

                text_pos = (int(20 + hand_center.x * image.shape[1]), int(-20+ hand_center.y * image.shape[0]))
                
                if all_fingers_raised == True:
                    if abs(delta_x) > 0.3:
                        next_tab()

                elif index_middle_distance < 0.1 and index_finger_is_straight:
                    if delta_y > 0.08:
                        vel = delta_y * 10
                        image = draw_text(image, "向上滑动", text_pos, font)
                    elif delta_y < -0.08:
                        vel = delta_y * 1
                        image = draw_text(image, "向下滑动", text_pos, font)
                    else:
                        image = draw_text(image, "滑动中", text_pos, font)
                else:
                    mouse_x = mouse_x + (index_finger.x * image.shape[1] * 5 - 300 - mouse_x) * 0.2
                    mouse_y = mouse_y + (index_finger.y * image.shape[0] * 5 - 300 - mouse_y) * 0.2
                    mouse.position = mouse_x, mouse_y

                    if index_finger_mcp.x - thumb.x < 0.06:
                        if not is_left_click:
                            left_down()
                            is_left_click = True
                            image = draw_text(image, "点击！", text_pos, font)
                    else:
                        if is_left_click:
                            left_up()
                            is_left_click = False
                        image = draw_text(image, "移动", text_pos, font)
                    draw_circulating_arcs(image, index_finger_pos, 20, angle1=angle1, angle2=angle2)
                scale_factor = 0.2

                scaled_landmarks = []
                for landmark in hand_landmarks.landmark:
                    scaled_x = int((landmark.x * image.shape[1] - rect3_center_x) * scale_factor + rect3_center_x -50)
                    scaled_y = int((landmark.y * image.shape[0] - rect3_center_y) * scale_factor + rect3_center_y+30)
                    scaled_landmarks.append((scaled_x, scaled_y))

                for connection in mp_hands.HAND_CONNECTIONS:
                    start_point = scaled_landmarks[connection[0]]
                    end_point = scaled_landmarks[connection[1]]
                    cv2.line(image, start_point, end_point, (0, 192, 255), 2)

                for landmark in scaled_landmarks:
                    cv2.circle(image, landmark, 2, (255, 255, 255), -1)

        image = draw_text(image, "iMouse", (30, 20), font2, (255, 255, 255))
        image = draw_text(image, "位置: " + str(int(mouse_x)) + ", " + str(int(mouse_y)) + " | 速度: " + str(int(delta_x*delta_x*delta_y*delta_y*1000000000)/100) + "cm/s", (190, 28), font3)
        aspect_ratio = frame.shape[1] / frame.shape[0]
        if screen_width / screen_height > aspect_ratio:
            new_height = screen_height
            new_width = int(screen_height * aspect_ratio)
        else:
            new_width = screen_width
            new_height = int(screen_width / aspect_ratio)

        resized_image = cv2.resize(image, (new_width, new_height))
        cv2.imshow("Hand Gestures", resized_image)

        # Exit the program if 'q' is pressed
        if is_key_pressed('esc'):
            break
        if cv2.waitKey(1) == 27:
            break

        angle1 = (angle1 + angle_increment) % 360
        angle2 = (angle2 - angle_increment) % 360

cap.release()
cv2.destroyAllWindows()
