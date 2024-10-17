
import RPi.GPIO as GPIO
import threading
import time

button_pins = [16, 20, 21]
button_flag = [False, False, False]
moterPin = [[6, 13, 19, 26], [5, 11, 9, 10], [2, 3, 4, 17]]

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
speed = 0.001

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
            button_flag_lock.acquire()
            flag = button_flag[0]
            button_flag_lock.release()
            
            if(flag) :
                for pin in range(4):
                    xpin = moterPin[moter][pin]
                    if Seq[StepCounter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                
                StepCounter += 1
                
                if StepCounter == StepCount:
                    StepCounter = 0

            speed_lock.acquire()
            now_speed = speed
            speed_lock.release()

            time.sleep(now_speed)
        time.sleep(2)
    

##########버튼 입력 read############
def inputButton(channel) :
    button_flag_lock.acquire()
    button_flag[0] = not button_flag[0]
    print(f"{button_flag[0]}")
    button_flag_lock.release()

def speedButton(channel) :
    global speed
    global speed_lock
    speed_lock.acquire()
    speed += 0.001
    print(f"{speed}")
    speed_lock.release()

def initeButton(channel) :
    global speed
    global speed_lock
    speed_lock.acquire()
    speed = 0.001
    print(f"{speed}")
    speed_lock.release()

def main() : 
    # Event 방식으로 핀의 Rising 신호를 감지하면 button_callback 함수를 실행
    GPIO.add_event_detect(button_pins[0],GPIO.RISING,callback=inputButton, bouncetime=300)
    #GPIO.add_event_detect(button_pins[1],GPIO.RISING,callback=lambda button:inputButton(1), bouncetime=300)
    #GPIO.add_event_detect(button_pins[2],GPIO.RISING,callback= lambda button:inputButton(2), bouncetime=300)

    GPIO.add_event_detect(button_pins[1],GPIO.RISING,callback=speedButton, bouncetime=300)
    GPIO.add_event_detect(button_pins[2],GPIO.RISING,callback=initeButton, bouncetime=300)

    moters = []
    for idx in range(3) :
        moters.append(threading.Thread(target= stepper_step, args=(idx, )))
        moters[idx].start()
    
    for moter in moters :
        moter.join()

if __name__ == "__main__" :
    main()