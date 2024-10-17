import time
import board
import neopixel

# LED 설정
LED_COUNT = 8  # CJMCU-2812B 모듈에는 8개의 LED가 있습니다.
PIN = board.D18  # 신호 핀에 맞게 설정 (Raspberry Pi의 GPIO 18번 핀)

# 네오픽셀 초기화
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=0.5, auto_write=False)

# 색상 정의
def color_wipe(color, wait_ms=50):
    for i in range(LED_COUNT):
        pixels[i] = color
        pixels.show()
        time.sleep(wait_ms / 1000.0)

try:
    while True:
        # 빨강
        color_wipe((255, 0, 0))  # 빨간색
        time.sleep(1)
        # 초록
        color_wipe((0, 255, 0))  # 초록색
        time.sleep(1)
        # 파랑
        color_wipe((0, 0, 255))  # 파란색
        time.sleep(1)
        # 무지개 색상 변경
        for i in range(LED_COUNT):
            pixels[i] = (i * 32, 255 - i * 32, i * 16)
        pixels.show()
        time.sleep(2)

except KeyboardInterrupt:
    # 프로그램이 종료될 때 LED를 모두 끕니다.
    color_wipe((0, 0, 0))
