import cv2
import mqtt.publish as publish
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    "haarcascades/haarcascade_frontalface_default.xml")
#faces = face_cascade.detectMultiScale(gray)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # ret, frame = cap.read()
    frame = cv2.imread('facetest.jpg')
    # if not ret:
    #     print("Cannot receive frame")
    #     break
    frame = cv2.resize(frame, (1200, 800))              # 縮小尺寸，避免尺寸過大導致效能不好
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # 將鏡頭影像轉換成灰階
    faces = face_cascade.detectMultiScale(gray)
    publish.publish(len(faces), "openfind1")
      # 偵測人臉
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)   # 標記人臉
    # cv2.imshow('img', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
