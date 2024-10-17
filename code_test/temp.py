import time
import spidev

# SPI 설정
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device)
spi.max_speed_hz = 8000000  # SPI 속도 설정

# 네오픽셀 데이터 전송 함수
def send_neopixel_data(data):
    spi.xfer2(data)  # SPI로 데이터 전송

# 예시: 8개의 네오픽셀을 빨간색으로 설정
num_pixels = 8
red_pixel_data = [255, 0, 0] * num_pixels  # 각 픽셀에 RGB 값 설정

send_neopixel_data(red_pixel_data)

# 지연 후 색상 변경
time.sleep(1)

# 예시: 8개의 네오픽셀을 파란색으로 설정
blue_pixel_data = [0, 0, 255] * num_pixels

send_neopixel_data(blue_pixel_data)
