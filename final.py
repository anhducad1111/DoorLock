import numpy as np
import track_hand as htm
import cv2
import urllib
import controller as cnt
import time

url = "http://192.168.58.130/cam-hi.jpg"

wCam, hCam = 800, 600
frameR = 100
detector = htm.handDetector(maxHands=1)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Mật khẩu
password = [4, 5, 2, 1, 3]
entered_code = []

def capture_image(frame):
    img_name = "hand_image_{}.png".format(int(time.time()))
    cv2.imwrite(img_name, frame)
    print("Đã chụp ảnh:", img_name)

while True:
    fingers = [0, 0, 0, 0, 0]
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        fingers = detector.fingersUp()
        
    cnt.led(fingers)
    
    # Phát hiện khuôn mặt
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
    # Thêm giá trị mới vào danh sách nếu khác 0
    sum_fingers = sum(fingers)
    if sum_fingers != 0 and sum_fingers not in entered_code:
        entered_code.append(sum_fingers)
    print(entered_code)
    
    # So sánh mảng nhập và mật khẩu
    if len(entered_code) == len(password):
        if entered_code == password:
            if len(faces) > 0:  # Nếu có mặt người được phát hiện
                capture_image(img)
                cnt.open_door()  
            else:
                print('dont have face')
                time.sleep(2)
                    
        else: 
            time.sleep(2)
        entered_code = []    
     
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)

    cv2.putText(img, "Number of fingers: " + str(sum(fingers)),
                (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
