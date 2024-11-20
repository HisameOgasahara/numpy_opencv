from PyQt5 import QtWidgets, uic, QtGui
import sys
import cv2
import numpy as np

class MyApp(QtWidgets.QDialog):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('qt_test.ui', self)
        self.count = 0

        #버튼
        self.loadBtn = self.findChild(QtWidgets.QPushButton, 'loadBtn')
        self.loadBtn.clicked.connect(self.loadBtnClicked) 
        self.procBtn = self.findChild(QtWidgets.QPushButton, 'procBtn')
        self.procBtn.clicked.connect(self.procBtnClicked) 

        self.src = self.findChild(QtWidgets.QLabel, 'imgSrc')     


        self.dst = self.findChild(QtWidgets.QLabel, 'imgDst')     
        self.filePath = self.findChild(QtWidgets.QLineEdit,'filePath')
        self.filePath.clear()
        self.show()

    # 이미지 로드(Image load)
    def loadBtnClicked(self):
        path = './images'
        filter = "All Images(*.jpg; *.png; *.bmp);;JPG (*.jpg);;PNG(*.png);;BMP(*.bmp)"
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "파일불러오기", path, filter)
    
        self.filename = str(fname[0])
        self.filePath.setText(self.filename)
        self.src.setPixmap(QtGui.QPixmap(self.filename))
        self.src.setScaledContents(True)
        self.count += 1 

    
    def procBtnClicked(self):
        if self.count != 0:
            img = self.imread(self.filename) #opencv는 한글 지원 안함
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            outImg = self.processingImage(img_rgb, img_gray)
            self.displayOutputImage(outImg)
        else:
            self.filename = "파일을 로드 하세요"
            self.filePath.setText(self.filename)

    #결과 이미지 출력
    def displayOutputImage(self, outImage):
        img_info = outImage.shape
        if outImage.ndim == 2 : # 그래이 영상
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], 
                            img_info[1]*1, QtGui.QImage.Format_Grayscale8)
        else :
            qImg = QtGui.QImage(outImage, img_info[1], img_info[0], 
                            img_info[1]*img_info[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.imgDst.setPixmap(pixmap)
        self.imgDst.setScaledContents(True)

    #한글 포함된 이미지 파일 읽어오기
    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8): 
        try: 
            n = np.fromfile(filename, dtype) 
            img = cv2.imdecode(n, flags) 
            return img 
        except Exception as e: 
            print(e) 
            return None

    def processingImage(self, img_rgb, img_gray):
        #여기에 여러분이 작성할 코드를 넣으시면 됩니다.
        outImg = img_gray
        return outImg

app = QtWidgets.QApplication(sys.argv)
window = MyApp()
app.exec_()