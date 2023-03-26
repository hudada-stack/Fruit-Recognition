import cv2
# from PIL import Image
import numpy as np
import os


'''
def sizeimage(image):

    nums = image.shape
    rows = nums[0]
    cols = nums[1]
    cropped = image[int((2/5)*rows):int((4/5)*rows), int((2/5)*cols):int((4/5)*cols)]  # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imshow('test',cropped)
    cv2.imwrite("image_  date/cv_cut_thor.jpg", cropped)
    image1 = Image.open('image_date/cv_cut_thor.jpg')

    ims_path = 'C:\\Users\\hudada\\PycharmProjects\\image_deal\\image_date\\'  # 图像数据集的路径
    ims_list = os.listdir(ims_path)
    R_means = []
    G_means = []
    B_means = []
    for im_list in ims_list:
        im = cv2.imread(ims_path + im_list)
        # extrect value of diffient channel
        im_R = im[:, :, 0]
        im_G = im[:, :, 1]
        im_B = im[:, :, 2]
        # count mean for every channel
        im_R_mean = np.mean(im_R)
        im_G_mean = np.mean(im_G)
        im_B_mean = np.mean(im_B)
        # save single mean value to a set of means
        R_means.append(im_R_mean)
        G_means.append(im_G_mean)
        B_means.append(im_B_mean)
        print('图片：{} 的 RGB平均值为 \n[{}，{}，{}]'.format(im_list, im_R_mean, im_G_mean, im_B_mean))












image=cv2.imread("source_imagedata/apple.png")
sizeimage(image)
'''


def process(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # RGB转HSV
    hsv = cv2.medianBlur(hsv, 5)
    # cv2.imshow("hsv",hsv)

    mask = cv2.inRange(hsv, (35, 43, 46), (77, 255, 255)) + cv2.inRange(hsv, (78, 43, 46), (99, 255, 255))  # 西瓜
    mask = cv2.inRange(hsv, (0, 43, 46), (10, 255, 255)) + cv2.inRange(hsv, (159, 43, 46), (180, 255, 255))  # 这是苹果
    # mask = cv2.inRange(hsv, (20, 43, 46), (70, 255, 255)) #这是香蕉的
    # mask = cv2.inRange(hsv, (8, 40, 40), (25, 255, 255))  # 这是橘子的

    # mask = cv2.inRange(hsv, (8, 40, 40), (25, 255, 255))  #这是橘子的
    line = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5), (-1, -1))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, line)
    cv2.imshow("mask", mask)

    # 轮廓提取, 发现最大轮廓
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
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, "orange", (x, y), font, 1.2, (0, 0, 255), 2)
    return image


image = cv2.imread("C:\\Users\\hudada\\PycharmProjects\\imagedeal\\source_imagedata\\apple.png")
result = process(image)
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

