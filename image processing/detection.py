import cv2
face_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
noseCascade = cv2.CascadeClassifier("haarcascade/Nariz.xml")
mouth_cascade= cv2.CascadeClassifier("haarcascade/haarcascade_mcs_mouth.xml")
face_mask = cv2.CascadeClassifier("cascadedownload/cascade.xml")

bw_threshold = 100
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(1)

while 1:
    ref, img = cap.read()
    img = cv2.flip(img, 1)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)

    if(len(faces)== 0 and len(faces_bw) == 0):
        cv2.putText(img, 'Tidak Ada Orang', (250,50), font,1,(255,0,0),2)
    else:
        for(x,y,w,h) in faces:
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
            nose_rects = noseCascade.detectMultiScale(gray, 1.5, 5)
            mask_rects = face_mask.detectionMultiScale(gray, 1.5, 5)

        if(len(mouth_rects)== 0 and len(nose_rects) == 0):
            cv2.putText(img, 'Menggunakan Masker',(170, 50), font,1,(0,255,0),2)
            cv2.putText(img, "100%",(50, 250), font,1,(250,255,0),2)
            cv2.putText(img, "Hidung Dan Mulut Tertutup",(150, 450),font,1,(250,255,0),2)
            cv2.rectangle(img,(x,y), (x+w, y+h), (0,255,0), 5)

            for (mx, my, mw, mh) in mask_rects:
                if(y<my<y+h):
                    cv2.putText(img, 'Masker',(mx,my),font,0.5,(250,255,0),2)
                    cv2.rectangle(img, (mx,my), (mx+mw, my+mh), (250, 255, 0),2)
                    break

                elif(len(mouth_rects)==0 and len(nose_rects) !=0 ):
                    cv2.putText(img, 'Penggunaan Masker Salah',(150,50),font,1,(0,255,255),2)
                    cv2.putText(img, '50%', (50,250), font,1,(250,255,0),2)
                    cv2.putText(img, 'Hidung Tidak Tertutup',(150,450),font,1,(0,0,255),2)
                    cv2.putText(img,(x,y),(x+w, y+h), (0,255,255),5)
                    
                    for(mx, my, mw, mh) in nose_rects:
                        if(y<my<y+h):
                            cv2.rectangle(img,(mx,my), (mx+mw, my+mh),(0,0,255),2)
                            break

                elif(len(mouth_rects)!=0 and len(nose_rects)==0):
                    cv2.putText(img, 'Penggunaan Masker Salah',(150,50),font,1,(0,251, 255),2)
                    cv2.putText(img,'50%',(50,250),font,1,(250, 255, 0),2)
                    cv2.putText(img, 'Mulut Tidak Tertutup',(150, 450), font,1(0,0,255),2)
                    cv2.rectangle(img, (x,y),(x+w, y+h), (0,255,255), 5)

                    

