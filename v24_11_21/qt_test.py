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

        self.trackbar.valueChanged.connect(self.dial.setValue)

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

    def on_trackbar(x):
        pass

    def processingImage(self, img_rgb, img_gray):

        img_src = img_rgb
        height, width = img_src.shape[:2]

        img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)


        # 1. 트랙바가 포함되어 있는 윈도우를 생성
        cv2.namedWindow("TrackBar")  # 윈도우의 이름을 계속 사용

        # 2. 트랙바를 몇개만들것인가 정함
        # cv2.createTrackbar("트랙바이름", "윈도우이름", 최소값,최대값, 호출함수)
        # 트랙바를 움직이면 바로 적용될때
        cv2.createTrackbar("threshold", "TrackBar", 0,255, self.on_trackbar) 
        # 특별한 이벤트를 적용하지 않을때
        cv2.createTrackbar("maxValue", "TrackBar", 0,255, lambda x : x) 

        # 3. 트랙바의 초기값 설정
        # cv2.setTrackbarPos("트랙바이름","윈도우이름", 초기값) 
        cv2.setTrackbarPos('threshold',"TrackBar", 127)
        cv2.setTrackbarPos('maxValue',"TrackBar", 255)

        # 4. 트랙바는 무한루프를 통해 연속적으로 변해야 함
        while cv2.waitKey(1) != ord('q'):
            # 5. 트랙바 값을 변수로 대입
            # 변수이름 = cv2.getTrackbarPos("트랙바이름","윈도우이름")
            thr_value = cv2.getTrackbarPos('threshold','TrackBar')
            mav_value = cv2.getTrackbarPos('maxValue','TrackBar')
            ret, img_dst = cv2.threshold(img_gray, thr_value, mav_value, cv2.THRESH_BINARY)
            img_dst = cv2.bitwise_not(img_dst)
            cv2.imshow('TrackBar',img_dst)

        outImg = img_gray
        return outImg

app = QtWidgets.QApplication(sys.argv)
window = MyApp()
app.exec_()