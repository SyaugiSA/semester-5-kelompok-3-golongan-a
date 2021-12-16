import numpy as np
import random
import cv2
import lockdoor

face_cascade = cv2.CascadeClassifier('myhaar.xml')
mouth_cascade = cv2.CascadeClassifier('Mouth.xml')
bw_threshold = 80

count = 0
font = cv2.FONT_HERSHEY_SIMPLEX
org = (30, 30)
weared_mask_font_color = (255, 0, 0)
not_weared_mask_font_color = (0, 0, 255)
noface = (255, 255, 255)
thickness = 2
font_scale = 1
weared_mask = "Menggunakan Masker"
not_weared_mask = "Tidak Menggunakan Masker"

##cap = cv2.imread('')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    # mematikan lampu dan lock door
    lockdoor.reset()

    ret, img = cap.read() ##Membaca Input
    img = cv2.flip(img,1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Mengkonfersi gambar menjadi grayscale
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)

    if(len(faces) == 0 and len(faces_bw) == 0):
        cv2.putText(img, "Tidak Terdeteksi Wajah...", org, font, font_scale, noface, thickness, cv2.LINE_AA)
    elif(len(faces) == 0 and len(faces_bw) == 1):
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        # terbuka
        lockdoor.terbuka()

    else:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) ##jika inputnya cocok maka membounding
            roi_gray = gray[y:y + h, x:x + w] ## ROI gray dengan koordinatnya
            roi_color = img[y:y + h, x:x + w] ##ROI color dengan titik koordinatnya
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5) 

        if(len(mouth_rects) == 0):
            cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)

        else:
            for (mx, my, mw, mh) in mouth_rects:
                if(y < my < y + h):
                    cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                    # tidak terbuka
                    lockdoor.tidakTerbuka()

                    print("Image"+str(count)+"Tersimpan") ##Menyimpan Gambar
                    file="G:/My Drive/anaconda/picture/No_Mask/"+str(count)+".jpg" ##Gambar tersimpan di Google Drive
                    cv2.imwrite(file, img) ##Menuliskan gambar
                    count += 1 ##Dengan memasukkan gambar dengan angka ditambah 1
                    break
                
    cv2.imshow('Mask Detection', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()