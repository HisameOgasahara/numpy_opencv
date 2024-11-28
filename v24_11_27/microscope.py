
from PIL import Image
import cv2
import os
import numpy as np

# WebP 파일 경로
input_webp = "images/microscope.webp"
output_folder = "output"

# 출력 폴더 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# WebP 애니메이션 읽기
webp_image = Image.open(input_webp)

frame_index = 0
while True:
    # 프레임을 numpy 배열로 변환
    frame = cv2.cvtColor(np.array(webp_image), cv2.COLOR_RGBA2BGRA)
    
    # 프레임 저장
    output_path = os.path.join(output_folder, f"frame_{frame_index:03d}.png")
    cv2.imwrite(output_path, frame)
    print(f"Saved {output_path}")
    
    frame_index += 1

    # 다음 프레임으로 이동
    try:
        webp_image.seek(frame_index)
    except EOFError:
        break

print("All frames are saved.")
