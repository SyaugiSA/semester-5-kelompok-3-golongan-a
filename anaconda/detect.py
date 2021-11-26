# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 23:44:08 2021

@author: MSI
"""
import numpy as np
import random
import cv2

face_cascade = cv2.CascadeClassifier('myhaar.xml')
mouth_cascade = cv2.CascadeClassifier('Mouth.xml')
bw_threshold = 80

count = 0
font = cv2.FONT_HERSHEY_SIMPLEX
org = (30, 30)
weared_mask_font_color = (0, 255, 0)
not_weared_mask_font_color = (0, 0, 255)
noface = (255, 255, 255)
thickness = 2
font_scale = 1
weared_mask = "Menggunakan Masker"
not_weared_mask = "Tidak Menggunakan Masker"

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    img = cv2.flip(img,1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)
    if(len(faces) == 0 and len(faces_bw) == 0):
        cv2.putText(img, "Tidak Terdeteksi Wajah...", org, font, font_scale, noface, thickness, cv2.LINE_AA)
    elif(len(faces) == 0 and len(faces_bw) == 1):
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
    else:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
        if(len(mouth_rects) == 0):
            cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        else:
            for (mx, my, mw, mh) in mouth_rects:
                if(y < my < y + h):
                    cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                    
                    print("Image"+str(count)+"Tersimpan")
                    file="F:/anaconda/picture/No_Mask/"+str(count)+".jpg"
                    cv2.imwrite(file, img)
                    count += 1
                    break
                
    cv2.imshow('Mask Detection', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()