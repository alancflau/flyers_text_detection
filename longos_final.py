import numpy as np
import cv2
import pandas as pd

import pytesseract
import re
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# img = cv2.imread('flyers/whole_foods_jan12-18_pg1.jpg', 1)

img = cv2.imread('flyers/longos-flyer-january-27-to-february-91-1.jpg', 1)
img = cv2.resize(img, (0,0), fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0,0,0])
upper = np.array([179,51,109])
mask = cv2.inRange(imgHSV, lower, upper) # filter out image of that color


imgResult = cv2.bitwise_and(img, img, mask = mask)
# ret, new_img = cv2.threshold(imgResult, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
# '''
#         line  8 to 12  : Remove noisy portion
# '''
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Grayscale
# imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
# ret, thresh = cv2.threshold(imgBlur, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,17)) # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
# kernel = np.ones((5,5),np.uint8)
dilated = cv2.dilate(mask, kernel,  iterations = 7)  #  `dilate , more the iteration more the dilation
eroded = cv2.erode(dilated,kernel, iterations = 8)
# dilated = cv2.morphologyEx(mask, cv2.MORPH_HITMISS, kernel)

contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
roi_arr = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 8000:
        x, y, w, h = cv2.boundingRect(cnt)
        padding = 80
        cv2.rectangle(img, (x - padding, y - padding), (x + w + padding, y + h + padding), (0, 255, 0), 3)
        # cv2.rectangle(img, (x, y + padding), (x + w - padding, y + h + padding), (0, 255, 0), 3)
        roi = img[y:y + h, x:x + w]
        roi_arr.append(roi)

flyer_str = []
for i in roi_arr:
    i_gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    string = pytesseract.image_to_string(i_gray)
    flyer_str.append(string)


print(flyer_str)
print(len(flyer_str))

print('Number of contours' + str(len(contours)))
cv2.imshow("IMage", img)
cv2.imshow("dilated", cv2.resize(dilated, (0,0), fx=0.3,fy=0.3))
cv2.imshow("eroded", cv2.resize(eroded, (0,0), fx=0.3,fy=0.3))
cv2.imwrite("walmart_sample.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#
#
# def text_extraction():
#     without_empty_strings = [string for string in flyer_str if string != ""]
#     brand, product, serving, sale_price, reg_price, valid_dt = [], [], [], [], [], []
#     for prod in without_empty_strings:
#
#         temp_lst = prod.splitlines()
#         str_list = list(filter(None, temp_lst))  # remove all empty strings
#
#         if len(str_list) < 2:
#             continue
#
#         if str_list[1].endswith(('”', '™', '“')):
#             str_list[1] = str_list[1][:-1]
#
#         if str_list[2].endswith(('”', '™', '“', '*')):
#             str_list[1] = str_list[1] + " " + str_list[2]
#             str_list.pop(2)
#
#         str_list[1] = re.sub("\*", '', str_list[1])
#
#         # unit of measure
#         try:
#             unit_index = [idx for idx, val in enumerate(str_list) if re.search(r"\d+\s?(ml|-pack|g|L)$", val)][0]
#         except:
#             unit_index = None
#
#         # Sale Prices
#         sale_index = [idx for idx, val in enumerate(str_list) if 'sale' in val.lower()]
#
#         # Regular Prices
#         reg_index = [idx for idx, val in enumerate(str_list) if 'regular' in val.lower()]
#
#         # Valid Dates
#         valid_index = [idx for idx, val in enumerate(str_list) if 'valid' in val.lower()]
#         print(valid_index)
#
#         brand.append(str_list[0])  # brand
#         product.append(str_list[1])  # product
#         sale_price.append(str_list[sale_index[0]] if sale_index else '')
#         reg_price.append(str_list[reg_index[0]] if reg_index else '')
#         valid_dt.append(str_list[valid_index[0]] if valid_index else '')
#         serving.append(str_list[unit_index] if unit_index else '')
#
#     df = pd.DataFrame(data=list(zip(brand, product, serving, sale_price, reg_price, valid_dt)),
#                       columns=['Brand', 'Product', 'Unit', ' Sale Price', 'Regular Price', 'Valid Dates']
#                       )
#     return df

# df = text_extraction()
# print(df)
#
# df.to_csv('test.csv')
# cv2.imwrite("Sample.png", img)
# cv2.imshow('Image', img)
# cv2.imshow('Image Gray', imgGray)
# cv2.imshow('Image Blur', imgBlur)
# # cv2.imshow('Image Canny', imgCanny)
# cv2.imshow('Image Result', connected)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
