import numpy as np
import cv2
import pandas as pd

import pytesseract
import re
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv2.imread('flyers/whole_foods_jan12-18_pg1.jpg', 1)


def preprocess(image):
    """
    :param image:
    :return preprocessed image:
    """
    global img
    # Preprocess
    img = cv2.resize(image, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Grayscale
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
    ret, thresh = cv2.threshold(imgBlur, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    connected = cv2.dilate(thresh, kernel, iterations=8)
    return connected


def get_contours(image, imgdilated):
    contours, hierarchy = cv2.findContours(imgdilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    roi_arr = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 8000:
            x, y, w, h = cv2.boundingRect(cnt)
            padding = 0
            cv2.rectangle(image, (x, y + padding), (x + w, y + h + padding), (0, 255, 0), 3)
            roi = image[y:y + h, x:x + w]
            roi_arr.append(roi)
    return roi_arr


def get_products(lst):
    flyer_str = []
    for i in lst:
        i_gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        string = pytesseract.image_to_string(i_gray)
        flyer_str.append(string)
    return flyer_str


connected = preprocess(img)
roi_array = get_contours(img, connected)
flyer_str = get_products(roi_array)

def text_extraction():
    without_empty_strings = [string for string in flyer_str if string != ""]
    brand, product, serving, sale_price, reg_price, valid_dt = [], [], [], [], [], []
    for prod in without_empty_strings:

        temp_lst = prod.splitlines()
        str_list = list(filter(None, temp_lst))  # remove all empty strings

        if len(str_list) < 2:
            continue

        if str_list[1].endswith(('”', '™', '“')):
            str_list[1] = str_list[1][:-1]

        if str_list[2].endswith(('”', '™', '“', '*')):
            str_list[1] = str_list[1] + " " + str_list[2]
            str_list.pop(2)

        str_list[1] = re.sub("\*", '', str_list[1])

        # unit of measure
        try:
            unit_index = [idx for idx, val in enumerate(str_list) if re.search(r"\d+\s?(ml|-pack|g|L)$", val)][0]
        except:
            unit_index = None

        # Sale Prices
        sale_index = [idx for idx, val in enumerate(str_list) if 'sale' in val.lower()]

        # Regular Prices
        reg_index = [idx for idx, val in enumerate(str_list) if 'regular' in val.lower()]

        # Valid Dates
        valid_index = [idx for idx, val in enumerate(str_list) if 'valid' in val.lower()]
        print(valid_index)

        brand.append(str_list[0])  # brand
        product.append(str_list[1])  # product
        sale_price.append(str_list[sale_index[0]] if sale_index else '')
        reg_price.append(str_list[reg_index[0]] if reg_index else '')
        valid_dt.append(str_list[valid_index[0]] if valid_index else '')
        serving.append(str_list[unit_index] if unit_index else '')

    df = pd.DataFrame(data=list(zip(brand, product, serving, sale_price, reg_price, valid_dt)),
                      columns=['Brand', 'Product', 'Unit', ' Sale Price', 'Regular Price', 'Valid Dates']
                      )
    return df

df = text_extraction()
print(df)
#
# df.to_csv('test.csv')
# cv2.imwrite("Sample.png", img)
# cv2.imshow('Image', img)
# cv2.imshow('Image Gray', imgGray)
# cv2.imshow('Image Blur', imgBlur)
# # cv2.imshow('Image Canny', imgCanny)
# cv2.imshow('Image Result', connected)

cv2.waitKey(0)
cv2.destroyAllWindows()
