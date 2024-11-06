# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17xZTNu0oMUZ5XzSQuKeqU0eDCJYxppPO
"""

# pip install easyocr
#
# pip install opencv-python==4.5.4.60
#
# pip install opencv-contrib-python==4.5.4.60
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from easyocr import Reader
import cv2

# Đọc hình ảnh và thay đổi kích thước
img = cv2.imread('image7.jpg') # Đọc hình ảnh từ tệp image3.jpg
img = cv2.resize(img, (800, 600))  # Thay đổi kích thước hình ảnh thành 800x600 pixels
# Tải font chữ
fontpath = "./arial.ttf" # a
font = ImageFont.truetype(fontpath, 32) # Tải font Arial với kích thước 32
b,g,r,a = 0,255,0,0 # Định nghĩa màu chữ (xanh lá cây) và độ trong suốt
# Chuyển đổi hình ảnh sang grayscale
grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Chuyển đổi hình ảnh từ màu sang grayscale
# Làm mờ hình ảnh
blurred = cv2.GaussianBlur(grayscale, (5, 5), 0) # Áp dụng bộ lọc Gaussian để làm mờ hình ảnh
# Phát hiện các cạnh trong hình ảnh
edged = cv2.Canny(blurred, 10, 200)# Sử dụng thuật toán Canny để phát hiện cạnh với ngưỡng 10 và 200
# Đợi một phím bất kỳ để đóng cửa sổ hiển thị hình ảnh
cv2.waitKey(0)
cv2.destroyAllWindows() # Đóng tất cả các cửa sổ OpenCV
# Tìm contours trong hình ảnh edged
contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# Sắp xếp các contours theo diện tích giảm dần và lấy 5 contours lớn nhất
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
# Xác định hình chữ nhật bao quanh bảng số xe
for c in contours:
    perimeter = cv2.arcLength(c, True) # Tính chu vi của contour
    approximation = cv2.approxPolyDP(c, 0.02 * perimeter, True)  # Xấp xỉ contour bằng đa giác
    print(approximation) # In ra các điểm đa giác xấp xỉ contour
    if len(approximation) == 4: # Nếu đa giác có 4 cạnh (hình chữ nhật)
        number_plate_shape = approximation # Lưu lại hình chữ nhật
        break # Dừng vòng lặp khi tìm được hình chữ nhật
# Lấy tọa độ của hình chữ nhật
(x, y, w, h) = cv2.boundingRect(number_plate_shape) # Lấy tọa độ và kích thước của hình chữ nhật
number_plate = grayscale[y:y + h, x:x + w] # Cắt phần ảnh chứa bảng số xe từ ảnh grayscale
# Thực hiện OCR
reader = Reader(['en']) # Khởi tạo đối tượng OCR với ngôn ngữ tiếng Anh
detection = reader.readtext(number_plate) # Đọc văn bản từ phần ảnh chứa bảng số xe
# Hiển thị kết quả OCR
if len(detection) == 0:
    text = "Không thấy bảng số xe"
    img_pil = Image.fromarray(img) # Chuyển đổi từ dữ liệu ảnh OpenCV sang PIl
    draw = ImageDraw.Draw(img_pil) # Tạo một đối tượng vẽ trên ảnh
    draw.text((150, 500), text, font = font, fill = (b, g, r, a)) # Vẽ văn bản "Không thấy bảng số xe" trên ảnh
    img = np.array(img_pil) # Chuyển đổi từ PIL sang dữ liệu ảnh OpenCV
    #cv2.putText(img, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
    cv2.waitKey(0) # Chờ đợi một phím được nhấn (để hiển thị ảnh)
else:
    cv2.drawContours(img, [number_plate_shape], -1, (255, 0, 0), 3) # Vẽ hình chữ nhật bao quanh bảng số xe
    text ="Biển số: " + f"{detection[0][1]}" # Lấy văn bản của biển số xe được nhận diện
    img_pil = Image.fromarray(img) # Chuyển đổi từ dữ liệu ảnh OpenCV sang PIL
    draw = ImageDraw.Draw(img_pil) # Tạo một đối tượng vẽ trên ảnh
    draw.text((200, 500), text, font = font, fill = (b, g, r, a)) # Vẽ văn bản biển số xe trên ảnh
    img = np.array(img_pil) # Chuyển đổi từ PIL sang dữ liệu ảnh OpenCV
    #cv2.putText(img, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
    cv2.imshow('Plate Detection', img) # Hiển thị ảnh với kết quả nhận diện biển số xe
    cv2.waitKey(0) # Chờ đợi một phím được nhấn (để hiển thị ảnh)
    #cv2.waitKey(5) # Chờ 5 miligiây trước khi tiếp tục (đoạn này có thể được bỏ qua)