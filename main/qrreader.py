import cv2
import pyzbar.pyzbar as pyzbar
from django.shortcuts import render
import webbrowser

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if success:
        for code in pyzbar.decode(frame):
            my_code = code.data.decode('utf-8')
            print("인식 성공: ", my_code)
            webbrowser.open(my_code)
            

        cv2.imshow('cam', frame)

        key = cv2.waitKey(50)
        if key == 27:
            break

cap.release()
cv2.desctoyWindow(cap)