import ctypes, time
import cv2

cam = VideoCapture(0)
result, image = cam.read()
imwrite("GeeksForGeeks.jpg", image)

# pics = ['DoZM-9RA.jpg']
# pics.append("dsc_0085.jpg")
# pics.append("Battle Cry.jpg")
# pics.append("black and white 3_7.jpg")
# # pics.append("dsc_0085.jpg")
#
# SPI_SETDESKWALLPAPER = 20
# for pic in pics:
#   time.sleep(1)
#   print(ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, 'C:\\Users\\patri\\Desktop\\Backround Pics\\' + str(pic), 0))

