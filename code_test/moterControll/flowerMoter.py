import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)


GPIO.setmode(GPIO.BCM)
StepPins_open = [12, 16, 20, 21]
StepPins_close = [21, 20, 16, 12]

for pin in StepPins_open:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

Angle = 160//6
StepAngle = 1.8
steps = int(Angle/StepAngle)
dir = False

# 한칸을 돌기 위해 필요한 속도
speed = 0.002

Seq = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]


def stepper_step() :
    StepCounter = 0
    cnt = 0
    while (1) :
        global dir

        if dir :
            StepPins = StepPins_open
        else :
            StepPins = StepPins_close

        step = steps
        for _ in range(step) :
            for pin in range(4):
                xpin = StepPins[pin]
                if Seq[StepCounter][pin] != 0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)
            StepCounter += 1
            if StepCounter == 4:
                StepCounter = 0
            time.sleep(speed)
        
        cnt += 1
        if(cnt == 7) : 
            cnt =0
            dir = not dir
        time.sleep(1)
        
try:
    stepper_step()

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
