i= imread ('Test2.jpg')
gray = rgb2gray(i)

imshow (gray)
xlswrite('Coba1', gray)
