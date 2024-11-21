import cv2
import numpy as np
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
import sys

form_class = uic.loadUiType('qt_test_win_threshold.ui')[0]

class myMain(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle("GUI Program sample")
        self.btn_load.clicked.connect(self.btn_load_clicked)
        self.btn_run.clicked.connect(self.btn_run_clicked)
        self.line_file_path.clear()
        self.count = 0
        # spinbox와 slider 연결
        self.slider_thr.valueChanged.connect(self.threshold_value_changed)
        self.spin_thr.valueChanged.connect(self.threshold_value_changed)

        self.modelist = [cv2.THRESH_BINARY,
                         cv2.THRESH_BINARY_INV,
                         cv2.THRESH_TRUNC,
                         cv2.THRESH_TOZERO,
                         cv2.THRESH_TOZERO_INV,
                         cv2.THRESH_MASK,
                         cv2.THRESH_OTSU,
                         cv2.THRESH_TRIANGLE,
                         cv2.ADAPTIVE_THRESH_MEAN_C,
                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C]
        self.combo_threshold.currentIndexChanged.connect(self.combo_threshold_changed)
        index = self.combo_threshold.currentIndex()
        self.threshold_option = self.modelist[index]

    def combo_threshold_changed(self, text):
        index = self.combo_threshold.currentIndex()
        self.threshold_option = self.modelist[index]
        self.threshold_value_changed()

    def threshold_value_changed(self):
        if self.filename != '':
            sender = self.sender()
            if sender == self.slider_thr:
                self.spin_thr.setValue(self.slider_thr.value())
            elif sender == self.spin_thr:
                self.slider_thr.setValue(self.spin_thr.value())

            img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(img_gray, self.slider_thr.value(), 255, self.threshold_option)
            self.displayOutputImage(binary)
        else:
            self.line_file_path.setText('파일을 선택해주세요')

    # 이미지 로드(Image load)
    def btn_load_clicked(self):
        path = './images'
        filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
        fname = QFileDialog.getOpenFileName(self, "파일불러오기", path, filter)

        self.filename = str(fname[0])
        self.line_file_path.setText(self.filename)
        self.lbl_img_src.setPixmap(QtGui.QPixmap(self.filename))
        self.lbl_img_src.setScaledContents(True)
        self.count += 1

    def btn_run_clicked(self):
        if self.count != 0:
            self.img = self.imread(self.filename)  # opencv는 한글 지원 안함
            #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #outImg = self.processingImage(img_rgb, img_gray)
            self.threshold_value_changed()
            #self.displayOutputImage(outImg)
        else:
            self.filename = "파일을 로드 하세요"
            self.line_file_path.setText(self.filename)

    # 한글 포함된 이미지 파일 읽어오기
    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None

    # 결과 이미지 출력
    def displayOutputImage(self, outImage):
        img_info = outImage.shape
        if outImage.ndim == 2:  # 그래이 영상
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0],
                                img_info[1] * 1, QtGui.QImage.Format_Grayscale8)
        else:
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0],
                                img_info[1] * img_info[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.lbl_img_dst.setPixmap(pixmap)
        self.lbl_img_dst.setScaledContents(True)

    def processingImage(self, img_rgb, img_gray):
        # 여기에 여러분이 작성할 코드를 넣으시면 됩니다.
        outImg = img_gray
        return outImg

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = myMain()
    sys.exit(app.exec_())