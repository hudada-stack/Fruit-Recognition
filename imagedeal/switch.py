"""
用来前期预判断和设置HSV分割阈值
"""
import cv2
choice=["orange","apple","banana","watermelon","kiwi"]
temp_choice=[]
fina_choice=[]
def pre_judge(RGB_R,RGB_B,HSV_H):
    if RGB_R>200 :
        if RGB_B> 100:
            temp_choice=[choice[2]]
        else:
            if HSV_H>=10 :
                temp_choice=[choice[0]]
            else:
                temp_choice=[choice[1]]

    else :
        temp_choice=[choice[3],choice[4]] #这两不仅RGB像，HSV也像
    return temp_choice


watermelon1_low=(35, 43, 46)
watermelon1_high=(77, 255, 255)
watermelon2_low=(78, 43, 46)
watermelon2_high=(99, 255, 255)

apple1_low=(0, 43, 46)
apple1_high=(10, 255, 255)
apple2_low=(159, 43, 46)
apple2_high=(180, 255, 255)

banana_low=(20, 43, 46)
banana_high=(70, 255, 255)

orange_low=(8, 40, 40)
orange_high=(25, 255, 255)

def Calculate_area(image):
    I=image
    #I = cv2.imread('C:\\Users\\hudada\\PycharmProjects\\imagedeal\\source_imagedata\\kiwi.png')
    I2 = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)

    #cv2.imshow('v', I2)
    #cv2.waitKey(0)
    rows, columns = I2.shape
    for i in range(0, rows):
        for j in range(0, columns):
            if I2[i][j] > 225:
                I2[i][j] = 255
            else:
                I2[i][j] = 0

    #cv2.imshow('v2', I2)
    #cv2.waitKey(0)

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
    #print(wb)
    if(wb>0.5):
        fina_choice=choice[3]
    else:
        fina_choice=choice[4]

    #cv2.imshow('self.captured', mask)
    #cv2.waitKey(0)
    return fina_choice



def judge(temp_choice,image):
    if len(temp_choice)==1:
        fina_choice=temp_choice
    else:
        fina_choice=Calculate_area(image)
    return fina_choice


def select_mask(fina_choice,hsv):
    print (fina_choice)
    if fina_choice==['apple']:
        #
        mask = cv2.inRange(hsv, (0, 43, 46), (10, 255, 255)) + cv2.inRange(hsv, (159, 43, 46), (180, 255, 255))  # 这是苹果
    elif fina_choice==['banana']:
        mask = cv2.inRange(hsv, (20, 43, 46), (70, 255, 255)) #这是香蕉的
    elif fina_choice==['orange']:
        mask = cv2.inRange(hsv, (8, 40, 40), (25, 255, 255))  #这是橘子的
    elif fina_choice=='watermelon':
        mask = cv2.inRange(hsv, (35, 43, 46), (77, 255, 255)) + cv2.inRange(hsv, (78, 43, 46), (99, 255, 255))  # 西瓜
    elif fina_choice=='kiwi':
        mask = cv2.inRange(hsv, (8, 40, 40), (25, 255, 255))  # 这是橘子的
    return mask








