import cv2
import numpy as np
import urllib.request
import controller as cnt
from cvzone.HandTrackingModule import HandDetector
import time

# Initialize hand detector and face cascade
detector = HandDetector(detectionCon=0.8, maxHands=1)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# URL for IP camera
url = "http://192.168.95.130/cam-hi.jpg"

# Password and entered code initialization
password = [4, 5, 2, 1, 3]
entered_code = []

# Camera resolution and frame margin
wCam, hCam = 800, 600
frameR = 100

def capture_image(frame):
    img_name = f"hand_image_{int(time.time())}.png"
    cv2.imwrite(img_name, frame)
    print("Đã chụp ảnh:", img_name)

while True:
    # Fetch image from URL
    resp = urllib.request.urlopen(url)
    img_array = np.array(bytearray(resp.read()), dtype=np.uint8)
    frame = cv2.imdecode(img_array, -1)
    frame = cv2.flip(frame, 1)
    
    # Detect hands
    hands, img = detector.findHands(frame)
    
    # Detect faces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # Process detected hands
    if hands:
        lmList = hands[0]
        fingers_up = detector.fingersUp(lmList)
        cnt.led(fingers_up)
        sum_fingers = sum(fingers_up)
        
        if sum_fingers != 0 and sum_fingers not in entered_code:
            entered_code.append(sum_fingers)
            print(entered_code)
        
        if len(entered_code) == len(password):
            if entered_code == password:
                if len(faces) > 0:
                    capture_image(img)
                    cnt.open_door()
                else:
                    print('No face detected')
                    time.sleep(2)
            else:
                print('Incorrect password')
                time.sleep(2)
            entered_code = []
        
        # Draw frame and finger count
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        cv2.putText(img, f'Finger count: {sum_fingers}', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Display the frame
    cv2.imshow("frame", img)
    
    # Exit on 'k' key press
    if cv2.waitKey(1) == ord('k'):
        break

cv2.destroyAllWindows()