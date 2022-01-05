import numpy as np
import random
import cv2
from keras.models import load_model
import tensorflow
from matplotlib import pyplot as plt
#import lockdoor

model = load_model('model-017.model')

face_cascade = cv2.CascadeClassifier('cascade.xml') ##Memanggil Hasil Training
mouth_cascade = cv2.CascadeClassifier('Mouth.xml')
bw_threshold = 80

count = 0
font = cv2.FONT_HERSHEY_SIMPLEX  ##tipe font
org = (30, 30) ##Koordinat X dan Y Untuk Menampilkan Font Yang Akan Muncul
weared_mask_font_color = (255, 0, 0) ##warna font menggunakan masker
not_weared_mask_font_color = (0, 0, 255) ##warna font tidak menggunakan masker
noface = (255, 255, 255) ##warna font tidak terdeteksi wajah
thickness = 2  ##ketebalan
font_scale = 1  ##skala font
weared_mask = "Menggunakan Masker"
not_weared_mask = "Tidak Menggunakan Masker"

cap = cv2.VideoCapture(0) ##Menginisiliasasi Input 
while True:
    # mematikan lampu dan lock door
    #lockdoor.reset()

    ret, img = cap.read() ##Membaca Input Yang Telah Diinisilalisasi Inputnya
    img = cv2.flip(img,1) #fungsi untuk mencerminkan img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Proses Mengkonfersi gambar menjadi grayscale
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY) #Proses menggunakan treshold menjadi citra biner 
    faces = face_cascade.detectMultiScale(gray, 1.1, 4) ##Untuk Memulai Mendeteksi MultiScale Gray
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4) ##Untuk Memulai Mendeteksi MultiScale Black and WHite

    # histogram rgb
    # color = ('b','g','r')
    # for i,col in enumerate(color):
    #     histr = cv.calcHist([img],[i],None,[256],[0,256])
    #     plt.plot(histr,color = col)
    #     plt.xlim([0,256])
    # plt.show()

    # histogram garyscale
    # plt.hist(gray.ravel(),256,[0,256]); plt.show()

    # histogram black white
    # plt.hist(black_and_white.ravel(),256,[0,256]); plt.show()

    if(len(faces) == 0 and len(faces_bw) == 0):
        cv2.putText(img, "Tidak Terdeteksi Wajah...", org, font, font_scale, noface, thickness, cv2.LINE_AA)
        ##Menampilkan Teks Ketika Tidak Terdeteksi Wajah dengan menentukan tipe font, ukuran font tidak terdeteksi wajah,
        ##Dan warna font, ketebalan font
    elif(len(faces) == 0 and len(faces_bw) == 1):
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        
        ##Menampilkan Teks Ketika Menggunakan Masker dengan menentukan tipe font, ukuran font ketika memakai masker,
        ##warna font, ketebalan font
        
        # Membuka kunci
        #lockdoor.terbuka()

    else:
        for (x, y, w, h) in faces:
            
            face_img = gray[y:y+w,x:x+w] ##Image dengan kumpulan Titik Koordinatnya
            resized = cv2.resize(face_img,(100,100)) ## Image Di resize atau diperkecil
            normalized = resized/255.0 
            reshaped = np.reshape(normalized,(1,100,100,1))
            result = model.predict(reshaped)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) ##jika inputnya cocok maka membounding wajah
            roi_gray = gray[y:y + h, x:x + w] ## ROI gray dengan titik koordinatnya
            roi_color = img[y:y + h, x:x + w] ## ROI color dengan titik koordinatnya
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5) 

        if(len(mouth_rects) == 0):
            cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
            ##Menampilkan Teks Ketika Menggunakan Masker dengan menentukan tipe font, ukuran font ketika memakai masker,
            ##Dan warna font, ketebalan font

        else:
            for (mx, my, mw, mh) in mouth_rects:
                if(y < my < y + h):
                    cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                    ##Menampilkan Teks Ketika Tidak Menggunakan Masker dengan menentukan tipe font, ukuran font ketika tidak memakai masker,
                    ##warna font, ketebalan font
                    
                    # Kunci tidak terbuka
                    #lockdoor.tidakTerbuka()

                    print("Image"+str(count)+"Tersimpan") ##Menyimpan Gambar
                    file="G:/My Drive/anaconda/picture/No_Mask/"+str(count)+".jpg" ##Gambar tersimpan di Google Drive
                    cv2.imwrite(file, img) ##Menuliskan gambar
                    count += 1 ##Dengan memasukkan gambar dengan angka ditambah 1
                    break
                
    cv2.imshow('Mask Detection', img) ##Menampilkan display dengan nama Mask Detection
    k = cv2.waitKey(30) & 0xff 
    if k == 27:
        break
    
cap.release() ##Mengeksekusi Program
cv2.destroyAllWindows() ##Mengakhiri Semua Window