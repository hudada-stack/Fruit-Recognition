import cv2
# from PIL import Image
import numpy as np
import os



def Calculate_area(image):
    I=image
    #I = cv2.imread('C:\\Users\\hudada\\PycharmProjects\\imagedeal\\source_imagedata\\kiwi.png')
    I2 = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)

    cv2.imshow('v', I2)
    cv2.waitKey(0)
    rows, columns = I2.shape
    for i in range(0, rows):
        for j in range(0, columns):
            if I2[i][j] > 225:
                I2[i][j] = 255
            else:
                I2[i][j] = 0

    cv2.imshow('v2', I2)
    cv2.waitKey(0)

    mask = I2
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    index = -1
    max = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    for c in range(len(contours)):
        area = cv2.contourArea(contours[c])
        if area > max:
            max = area
            index = c
    # 绘制外接矩形
    if index >= 0:
        x, y, w, h = cv2.boundingRect(contours[index])
        cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(mask, "orange", (x, y), font, 1.2, (0, 0, 255), 2)

    num_black = 0
    num_white = 0

    for i in range(0, rows):
        for j in range(0, columns):
            if mask[i][j] > 0:
                num_white = num_white + 1
            else:
                num_black = num_black + 1

    wb = num_white / (num_black + num_white)
    print(wb)

    cv2.imshow('self.captured', mask)
    cv2.waitKey(0)

