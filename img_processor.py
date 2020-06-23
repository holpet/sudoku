import cv2.cv2 as cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
filename = 'img/test_sudokuboard.png'
img = cv2.imread(filename)
print(img.shape)
#imgCropped = img[0:400, 0:200]

 # Need to convert cv2 values BGR to RGB for standard reading
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edged = cv2.Canny(gray, 170, 200)
cv2.imshow("3 - Canny Edges", edged)
cv2.waitKey(0)

# Find contours based on Edges
cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Create copy of original image to draw all contours
img1 = img.copy()
cv2.drawContours(img1, cnts, -1, (0,255,0), 3)
cv2.imshow("4- All Contours", img1)
cv2.waitKey(0)

#sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]

for c in cnts:
    peri = cv2.arcLength(c, True)



text = pytesseract.image_to_string(img, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789', lang="eng")
print(text)

cv2.imshow("Image", gray)
cv2.waitKey()
