from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
import cv2
import numpy as np

class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('qt_test.ui', self)
        self.count = 0

        # 버튼
        self.loadBtn = self.findChild(QtWidgets.QPushButton, 'loadBtn')
        self.loadBtn.clicked.connect(self.loadBtnClicked)
        self.procBtn = self.findChild(QtWidgets.QPushButton, 'procBtn')
        self.procBtn.clicked.connect(self.procBtnClicked)

        # 트랙바 연결 (QSlider 사용)
        self.trackbar = self.findChild(QtWidgets.QSlider, 'trackbar') # 이름 변경
        if self.trackbar is not None: # trackbar가 존재하는지 확인
            self.trackbar.setOrientation(QtCore.Qt.Horizontal)
            self.trackbar.setMinimum(0)
            self.trackbar.setMaximum(255)
            self.trackbar.setValue(127)
            self.trackbar.valueChanged.connect(self.updateProcessedImage)
        else:
            print("Error: trackbar not found in UI file.")

        self.maxValueSlider = self.findChild(QtWidgets.QSlider, 'maxValueSlider') #maxValueSlider도 확인
        if self.maxValueSlider is not None:
            self.maxValueSlider.setOrientation(QtCore.Qt.Horizontal)
            self.maxValueSlider.setMinimum(0)
            self.maxValueSlider.setMaximum(255)
            self.maxValueSlider.setValue(255)
            self.maxValueSlider.valueChanged.connect(self.updateProcessedImage)
        else:
            print("Error: maxValueSlider not found in UI file.")


        self.src = self.findChild(QtWidgets.QLabel, 'imgSrc')
        self.dst = self.findChild(QtWidgets.QLabel, 'imgDst')
        self.filePath = self.findChild(QtWidgets.QLineEdit, 'filePath')
        self.filePath.clear()
        self.show()

    # ... (나머지 코드는 동일) ...

    # 이미지 로드 (Image load)
    def loadBtnClicked(self):
        path = './images'
        filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "파일불러오기", path, filter)

        self.filename = str(fname[0])
        self.filePath.setText(self.filename)
        self.src.setPixmap(QtGui.QPixmap(self.filename))
        self.src.setScaledContents(True)
        self.count += 1
        self.updateProcessedImage() # 이미지 로드 후 바로 처리된 이미지 보여주기


    def procBtnClicked(self): # 이 함수는 사실상 필요없어짐
        self.updateProcessedImage()


    # 결과 이미지 출력
    def displayOutputImage(self, outImage):
        img_info = outImage.shape
        if outImage.ndim == 2:  # 그레이 영상
            qImg = QtGui.QImage(outImage.data, img_info[1], img_info[0],
                                img_info[1] * 1, QtGui.QImage.Format_Grayscale8)
        else:
            qImg = QtGui.QImage(outImage.data, img_info[1], img_info[0],
                                img_info[1] * img_info[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.imgDst.setPixmap(pixmap)
        self.imgDst.setScaledContents(True)

    # 한글 포함된 이미지 파일 읽어오기
    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None

    def updateProcessedImage(self):
        if self.count == 0:
            self.filename = "파일을 로드 하세요"
            self.filePath.setText(self.filename)
            return

        img = self.imread(self.filename)
        if img is None:
            return

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thr_value = self.trackbar.value()
        mav_value = self.maxValueSlider.value()

        # 콤보 박스 선택에 따라 이진화 방법 변경
        threshold_type = self.comboBox.currentIndex()  # 현재 선택된 인덱스를 가져온다.

        # threshold type에 따른 처리
        if threshold_type == 0:  # THRESH_BINARY
            ret, img_dst = cv2.threshold(img_gray, thr_value, mav_value, cv2.THRESH_BINARY)
        elif threshold_type == 1:  # THRESH_BINARY_INV
            ret, img_dst = cv2.threshold(img_gray, thr_value, mav_value, cv2.THRESH_BINARY_INV)
        elif threshold_type == 2:  # THRESH_TRUNC
            ret, img_dst = cv2.threshold(img_gray, thr_value, mav_value, cv2.THRESH_TRUNC)
        elif threshold_type == 3:  # THRESH_TOZERO
            ret, img_dst = cv2.threshold(img_gray, thr_value, mav_value, cv2.THRESH_TOZERO)
        elif threshold_type == 4:  # THRESH_TOZERO_INV
            ret, img_dst = cv2.threshold(img_gray, thr_value, mav_value, cv2.THRESH_TOZERO_INV)
        elif threshold_type == 5:  # THRESH_OTSU
            ret, img_dst = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # Otsu's thresholding의 경우 thr_value와 mav_value는 필요없다.
        else:
            print("Invalid threshold type selected.")
            return

        self.displayOutputImage(img_dst)


app = QtWidgets.QApplication(sys.argv)
window = MyApp()
app.exec_()