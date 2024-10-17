import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
StepPins = [5, 11, 9, 10]

for pin in StepPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

StepCounter = 0
StepCount = 4

# 한칸을 돌기 위해 필요한 속도
speed = 0.01
step_sleep = 30 # 대강 speed * 0.01 sec

Seq = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]

def stepper_step() :
    global StepCounter
    
    for pin in range(4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin] != 0:
            GPIO.output(xpin, True)
        else:
            GPIO.output(xpin, False)
    
    StepCounter += 1
    
    if StepCounter == StepCount:
        StepCounter = 0
    #if StepCounter < 0:
    #   StepCounter = StepCount - 1
    
    time.sleep(speed)

try:
    while True:
        for step in range(step_sleep) :
            stepper_step()
        time.sleep(2)
            

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
