
import RPi.GPIO as GPIO
import threading
import time

button_pins = [16, 20, 21]
button_flag = [False, False, False]
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

print(steps)

# 한칸을 돌기 위해 필요한 속도
speed = 0.01

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# button_flag의 race condition을 해결하기 위함
button_flag_lock = threading.Lock()
speed_lock = threading.Lock()

for pin in button_pins :
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

for moter in moterPin:
    for pin in moter :
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

########모터 움직임 제어 함수#############
def stepper_step(moter) :
    StepCounter = 0
    counter = 0
    while (1) :
        step = steps
        counter += 1
        if counter%Section == 0 :
            counter = 0
        for _ in range(step) :
            
            for pin in range(4):
                xpin = moterPin[moter][pin]
                if Seq[StepCounter][pin] != 0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)
            
            StepCounter += 1
            
            if StepCounter == StepCount:
                StepCounter = 0

            time.sleep(speed)
        time.sleep(2)
    

def main() : 
    moters = []
    for idx in range(3) :
        moters.append(threading.Thread(target= stepper_step, args=(idx, )))
        moters[idx].start()
    
    for moter in moters :
        moter.join()

if __name__ == "__main__" :
    main()