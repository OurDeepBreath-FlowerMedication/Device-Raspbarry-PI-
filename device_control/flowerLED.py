import time
import board
import neopixel
import threading

pixel_pin = board.D18 # GPIO 설정  
num_pixels = 8 # 네오픽셀 LED 수

# 네오픽셀 초기화
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False)

# 색상 정의 (빨, 주, 노, 초, 파, 남, 보)
colors = [
    (255, 0, 0),
    (255, 50, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 100, 100),
    (0, 0, 255),
    (128, 0, 128),
    (255, 255, 255)
]

class FlowerLED :
    def __init__(self) :
        self.done = 0
        self.take_medi = False
        self.blankLock = threading.Lock()

    def startDay(self, all) :
        self.all = all
        pixels.fill(colors[0])
        pixels.show()

    def turnOff(self) :
        self.takeMedi()
        self.done = 0
        pixels.fill((0, 0, 0))
        pixels.show()

    def doneRoutine(self) :
        self.blankLock.acquire()
        self.done = self.done+1
        self.color_wipe()
        self.blankLock.release()

    def noticeLED(self) :
        blankThread = threading.Thread(target = self.colorBlank)
        blankThread.start()
    
    def takeMedi(self) :
        self.blankLock.acquire()
        self.take_medi = True
        self.blankLock.release()

    # 다음 색상으로 변경할때
    # LED를 순차적으로 점등하는 함수
    def color_wipe(self):
        color = int((self.done*7)//self.all)
        
        for i in range(num_pixels):
            pixels[i] = colors[color]
            pixels.show()      
            time.sleep(0.1)

    # LED가 깜빡임
    # 섭취할 약이 있음을 알리는 용도
    def colorBlank(self):
        self.take_medi = False
        while True :
            self.blankLock.acquire()
            if(self.take_medi) : 
                self.blankLock.release()
                break
            color = int((self.done*7)//self.all)
            self.blankLock.release()

            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(0.2)
            pixels.fill(colors[color])
            pixels.show()
            time.sleep(0.5)
            

