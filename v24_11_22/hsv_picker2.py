import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class HSVViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HSV Viewer")

        self.image_label = QLabel()
        self.hsv_label = QLabel()
        self.hsv_label.setAlignment(Qt.AlignCenter)
        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_image_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.hsv_label)
        self.setLayout(layout)

        self.image = None

    def open_image_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            self.open_image(filename)

    def open_image(self, filename):
        self.image = cv2.imread(filename)
        if self.image is None:
            print(f"Error: Could not load image from {filename}")
            self.hsv_label.setText("Error: Could not load image.")
            return

        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        height, width, channel = self.image.shape

        # 창의 최대 크기 설정 (예: 800x600)
        max_width = 800
        max_height = 600

        # 이미지의 가로 세로 비율 계산
        aspect_ratio = width / height

        # 이미지 크기 조정 (비율 유지)
        if width > max_width or height > max_height:
            if aspect_ratio > 1:  # 가로가 더 긴 경우
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:  # 세로가 더 긴 경우
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
        else:
            new_width = width
            new_height = height

        # 이미지 크기 조정 (cv2.resize 사용)
        resized_image = cv2.resize(self.image, (new_width, new_height))

        # QImage로 변환 및 QLabel에 설정
        bytesPerLine = 3 * new_width
        qImg = QImage(resized_image.data, new_width, new_height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)

        # QLabel에 pixmap 설정하고 중앙 정렬
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        # setScaledContents(True) 제거

        self.image_label.mousePressEvent = self.mouse_click
        self.hsv_label.setText("")
        self.resize(new_width, new_height) # 창 크기 조정 (이미지 크기에 맞춤)

    def mouse_click(self, event):
        if self.image is None:
            return

        x = event.pos().x()
        y = event.pos().y()

        if 0 <= x < self.image.shape[1] and 0 <= y < self.image.shape[0]:
            bgr_pixel = self.image[y, x]
            hsv_pixel = cv2.cvtColor(np.uint8([[bgr_pixel]]), cv2.COLOR_RGB2HSV)[0][0]
            hsv_text = f"HSV: H={hsv_pixel[0]:.0f}, S={hsv_pixel[1]:.0f}, V={hsv_pixel[2]:.0f}"
            self.hsv_label.setText(hsv_text)


if __name__ == "__main__":
    app = QApplication([])
    viewer = HSVViewer()
    viewer.show()
    app.exec_()