import cv2
import numpy as np
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication
import sys
import matplotlib
# from ctypes import cdll

# lib = cdll.LoadLibrary('Test.h')
# lib.main()



upper_blue = np.array([0, 0, 0])
lower_blue = np.array([255, 255, 255])

adder = 20

tracker = False
startX = 0
startY = 0
endX = 0
endY = 0


def removeSmallBlobs(img, minBlobSize):
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, None, None, None, 8, cv2.CV_32S)
    areas = stats[1:, cv2.CC_STAT_AREA]
    result = np.zeros(labels.shape, np.uint8)
    for i in range(0, nlabels - 1):
        if areas[i] >= minBlobSize:  # keep
            result[labels == i + 1] = 255
    return result


def checkImg(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = removeSmallBlobs(mask, 500)
    return result


cap = cv2.VideoCapture(0)

app = QApplication(sys.argv)
win = QWidget()
imgWid = QLabel(win)
filterWid = QLabel(win)
dataDisplay = QTextEdit(win)


def showImg(frame, wid):
    # ret, frame = cap.read()
    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
    convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
    pixmap = QPixmap(convertToQtFormat)
    wid.setPixmap(pixmap)

def updateGUI():
    ret, frame = cap.read()
    ff = frame.copy()
    if not tracker:
        cv2.rectangle(ff, (startX, startY), (endX, endY), (0, 255, 0), 2)
    showImg(ff, imgWid)
    # if not tracker:
    frame = checkImg(frame)
    showImg(frame, filterWid)
    filterWid.move(imgWid.width(), 0)
    filterWid.setFixedSize(frame.shape[1], frame.shape[0])

def updateValues():
    global upper_blue, lower_blue
    # pass
    ret, frame = cap.read()
    frame = frame[startY:endY, startX:endX]
    outB = []
    outG = []
    outR = []
    for i in range(256):
        for j in range(int(np.sum(frame[:, :, 0] == i))):
            outB.append(i)
        for j in range(int(np.sum(frame[:, :, 1] == i))):
            outG.append(i)
        for j in range(int(np.sum(frame[:, :, 2] == i))):
            outR.append(i)
    upper_blue = np.array([min(int(np.percentile(outR, 90) + adder), 255), min(int(np.percentile(outG, 90) + adder), 255), min(int(np.percentile(outB, 90) + adder), 255)])
    lower_blue = np.array([max(int(np.percentile(outR, 10) - adder), 0), max(int(np.percentile(outG, 10) - adder), 0), max(int(np.percentile(outB, 10) - adder), 0)])
    print("RGB: {0}, {1}".format(upper_blue, lower_blue))
    hsvUpper = matplotlib.colors.rgb_to_hsv([upper_blue[0] / 255, upper_blue[1] / 255, upper_blue[2] / 255])
    hsvUpper = np.array([int(hsvUpper[0] * 179), int(hsvUpper[1] * 255), int(hsvUpper[2] * 255)])
    hsvLower = matplotlib.colors.rgb_to_hsv([lower_blue[0] / 255, lower_blue[1] / 255, lower_blue[2] / 255])
    hsvLower = np.array([int(hsvLower[0] * 179), int(hsvLower[1] * 255), int(hsvLower[2] * 255)])
    print("HSV: {0}, {1}".format(hsvUpper, hsvLower))
    print()
    dataDisplay.setText("RGB: {0}, {1}\nHSV: {2}, {3}".format(upper_blue, lower_blue, hsvUpper, hsvLower))
    dataDisplay.move(0, imgWid.height())



def clickedOn(event: QMouseEvent):
    global startY, startX, tracker, endX, endY
    if tracker:
        endX = event.pos().x()
        endY = event.pos().y()
        a = min(endX, startX)
        aa = max(startX, endX)
        startX = a
        endX = aa
        a = min(endY, startY)
        aa = max(startY, endY)
        startY = a
        endY = aa

        tracker = False
        if startX == endX:
            endX += 1
        if startY == endY:
            endY += 1
        updateValues()
    else:
        startX = event.pos().x()
        startY = event.pos().y()
        tracker = True

updateGUI()
dataDisplay.setFixedHeight(50)
dataDisplay.move(-1000, -1000)
timer = QTimer()
timer.timeout.connect(updateGUI)
timer.start(10)

imgWid.mousePressEvent = clickedOn

win.show()
win.resize(1500, 700)
sys.exit(app.exec_())
