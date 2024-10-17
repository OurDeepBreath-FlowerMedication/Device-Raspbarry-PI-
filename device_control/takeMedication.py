
import RPi.GPIO as GPIO
import time
import API.callServer as cs

###### 기본 변수 설정(상수) #####
button = 23
button_flag = [False, False, False]

# 아침, 점심, 저녁 
moterPin = [[6, 13, 19, 26], [10, 9, 11, 5], [17, 4, 3, 2]]

Seq = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]

StepCount = 4
Section = 8
StepAngle = 1.8
Angle = int(360/Section)

steps = int(Angle/StepAngle)

# 한칸을 돌기 위해 필요한 속도
speed = 0.005
#############################

# GPIO 핀 설정 초기화
GPIO.setwarnings(False)

# GPIO 핀 모드
GPIO.setmode(GPIO.BCM)

# 버튼 핀 설정
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

# 모터 핀 설정
for moter in moterPin:
    for pin in moter :
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

########모터 움직임 제어 함수(버튼 누르면 수행)#############
def stepper_step(mealTime) :
    StepCounter = 0 # 섹션 구분(섹션 한 루프당 1.8 도)
    for _ in range(steps) :
        for pin in range(4):
            xpin = moterPin[mealTime][pin]
            if Seq[StepCounter][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        
        StepCounter += 1
        
        if StepCounter == StepCount:
            StepCounter = 0

        time.sleep(speed)

class TakeMedication : 
    def __init__(self, mealTime, flag, flowerLED, flowerMoter) :
        self.mealTime = mealTime 
        self.flag = flag
        self.is_activate = False
        self.flowerLED = flowerLED
        self.flowerMoter = flowerMoter
        self.routines = []

    def __del__(self) :
        GPIO.remove_event_detect(button)

    def activate_button(self, routines : list, routine : dict) :
        self.routines = routines
        self.routine = routine
        self.is_activate = True
        self.flowerLED.noticeLED()
        GPIO.add_event_detect(button, GPIO.RISING, callback=self.push_button, bouncetime=300)

    def deactivate_button(self) :
        # 재 실행을 막기 위해, 관련 정보 지우기
        self.routines.remove(self.routine)
        
        self.is_activate = False
        self.flowerLED.takeMedi()
        GPIO.remove_event_detect(button)

    def push_button(self, channel) :
        # 서버 업데이트
        cs.updateDone(self.routine['id'])
        # 모터가 움직였음을 나타냄
        self.flag = True
        self.flowerLED.doneRoutine()
        self.flowerMoter.blomming_flower()

        # 모터 한칸 움직임
        stepper_step(self.mealTime)
        self.deactivate_button()
        
        
    