import sys
import cv2
import os
import numpy as np
import switch
import baidufruit

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from fruit_recognition import Ui_MainWindow

se=[]
kkk=''
class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.cropped = None
        self.setupUi(self)

        self.camera = cv2.VideoCapture(0)
        self.is_camera_opened = False  # 摄像头有没有打开标记

        # 定时器：30ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(30)

    def btnOpenCamera_Clicked(self):
        '''
        打开和关闭摄像头
        '''
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self.btnOpenCamera.setText("关闭摄像头")
            self._timer.start()
        else:
            self.btnOpenCamera.setText("打开摄像头")
            self._timer.stop()

    def btnCapture_Clicked(self):
        '''
        捕获图片
        '''
        # 摄像头未打开，不执行任何操作
        if not self.is_camera_opened:
            return

        self.captured = self.frame
        # 后面这几行代码几乎都一样，可以尝试封装成一个函数
        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        # Qt显示图片时，需要先转换成QImgage类型
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnReadImage_Clicked(self):
        '''
        从本地读取图片 文件路径不能有中文
        '''
        # 打开文件选取对话框
        filename, _ = QFileDialog.getOpenFileName(self, '打开图片')
        if filename:
            self.captured = cv2.imread(str(filename))
            # OpenCV图像以BGR通道存储，显示时需要从BGR转到RGB
            self.captured = cv2.cvtColor(self.captured, cv2.COLOR_BGR2RGB)

            rows, cols, channels = self.captured.shape
            bytesPerLine = channels * cols
            QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
            self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnGray_Clicked(self):
        '''
        灰度化
        '''
        # 如果没有捕获图片，则不执行操作
        if not hasattr(self, "captured"):
            return
        self.cpatured = cv2.cvtColor(self.captured, cv2.COLOR_RGB2GRAY)
        rows, columns = self.cpatured.shape
        bytesPerLine = columns
        # 灰度图是单通道，所以需要用Format_Indexed8
        QImg = QImage(self.cpatured.data, columns, rows, bytesPerLine, QImage.Format_Indexed8)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnCrop_Clicked(self):
        #裁剪采用算平均RGB值
        global se
        if not hasattr(self, "captured"):
            return
        #self.cpatured = cv2.cvtColor(self.captured, cv2.COLOR_BGR2RGB)
        rows, cols, channels = self.captured.shape
        cropped = self.captured[int((2 / 5) * rows):int((4 / 5) * rows), int((2 / 5) * cols):int((4 / 5) * cols)]
        #cv2.imwrite("image_date/cv_cut_thor.jpg", cropped)
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        cv2.imwrite("image_date/cv_cut_thor.jpg", cropped)

        cropped=cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        new_rows, new_cols, new_channels=cropped.shape
        bytesPerLine = new_channels * new_cols
        QImg = QImage(cropped.data, new_cols, new_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        ims_path = 'C:\\Users\\hudada\\PycharmProjects\\imagedeal\\image_date\\'  # 图像数据集的路径
        ims_list = os.listdir(ims_path)
        R_means = []
        G_means = []
        B_means = []
        for im_list in ims_list:
            im = cv2.imread(ims_path + im_list)
            im=cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
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

        for im_list in ims_list:
            im = cv2.imread(ims_path + im_list)
            im=cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            im=cv2.cvtColor(im,cv2.COLOR_RGB2HSV)
            # extrect value of diffient channel
            im_H = im[:, :, 0]
            im_S = im[:, :, 1]
            im_V = im[:, :, 2]
            # count mean for every channel
            im_H_mean = np.mean(im_H)
            im_S_mean = np.mean(im_S)
            im_V_mean = np.mean(im_V)
            # save single mean value to a set of means
            R_means.append(im_H_mean)
            G_means.append(im_S_mean)
            B_means.append(im_V_mean)
            print('图片：{} 的 HSV平均值为 \n[{}，{}，{}]'.format(im_list, im_H_mean, im_S_mean, im_V_mean))
        print("第一次判断结果为：")
        print(switch.pre_judge(im_R_mean, im_B_mean,im_H_mean))
        print("最终判断结果为：")
        print(switch.judge(switch.pre_judge(im_R_mean, im_B_mean,im_H_mean),self.captured))
        se =switch.judge(switch.pre_judge(im_R_mean, im_B_mean,im_H_mean),self.captured)
        #return switch.fina_choice


    def btnOutline_Clicked(self):
        '''
        轮廓提取
        '''
        if not hasattr(self, "captured"):
            return

        hsv = cv2.cvtColor(self.captured, cv2.COLOR_RGB2HSV)  # RGB转HSV
        hsv = cv2.medianBlur(hsv, 5)
        #cv2.imshow("hsv", hsv)

        mask=switch.select_mask(se, hsv)

        # mask = cv2.inRange(hsv, (35, 43, 46), (77, 255, 255))+cv2.inRange(hsv, (78, 43, 46), (99, 255, 255))#西瓜
        #mask = cv2.inRange(hsv, (0, 43, 46), (10, 255, 255)) + cv2.inRange(hsv, (159, 43, 46), (180, 255, 255))  # 这是苹果
        # mask = cv2.inRange(hsv, (20, 43, 46), (70, 255, 255)) #这是香蕉的

        # mask = cv2.inRange(hsv, (8, 40, 40), (25, 255, 255))  #这是橘子的
        line = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5), (-1, -1))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, line)
        #cv2.imshow("mask", mask)

        rows, columns = mask.shape
        bytesPerLine = columns
        # 灰度图是单通道，所以需要用Format_Indexed8
        QImg = QImage(mask.data, columns, rows, bytesPerLine, QImage.Format_Indexed8)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnRec_Clicked(self):
        if not hasattr(self, "captured"):
            return


        hsv = cv2.cvtColor(self.captured, cv2.COLOR_RGB2HSV)  # RGB转HSV
        hsv = cv2.medianBlur(hsv, 5)
        # cv2.imshow("hsv",hsv)

        mask = switch.select_mask(se, hsv)

        #mask = cv2.inRange(hsv, (35, 43, 46), (77, 255, 255)) + cv2.inRange(hsv, (78, 43, 46), (99, 255, 255))  # 西瓜
        #mask = cv2.inRange(hsv, (0, 43, 46), (10, 255, 255)) + cv2.inRange(hsv, (159, 43, 46), (180, 255, 255))  # 这是苹果
        # mask = cv2.inRange(hsv, (20, 43, 46), (70, 255, 255)) #这是香蕉的
        # mask = cv2.inRange(hsv, (8, 40, 40), (25, 255, 255))  # 这是橘子的

        # mask = cv2.inRange(hsv, (8, 40, 40), (25, 255, 255))  #这是橘子的
        line = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5), (-1, -1))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, line)
        #cv2.imshow("mask", mask)

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
            cv2.rectangle(self.captured, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(self.captured, str(se).strip('[]'), (x, y), font, 1.2, (0, 0, 255), 2)
        #cv2.imshow('self.captured',self.captured)
        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.labelResult.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelResult.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnBaidu_Clicked(self):
        global kkk
        if not hasattr(self, "captured"):
            return
        kkk=baidufruit.baidusearch(self.captured)
        print(kkk)
        s=kkk[50:63]
        self.labelResult.setText(s)




    @QtCore.pyqtSlot()
    def _queryFrame(self):

        ret, self.frame = self.camera.read()
        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())