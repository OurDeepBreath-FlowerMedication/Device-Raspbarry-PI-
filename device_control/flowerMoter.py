import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
StepPins_close = [12, 16, 20, 21]
StepPins_open = [21, 20, 16, 12]

for pin in StepPins_open:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

Angle = 180
StepAngle = 1.8
speed = 0.002
Seq = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]

class FlowerMoter :
    def startDay(self, all) :
        self.steps = int((Angle/all)/StepAngle)
        self.cur = 0

    # 단계 별로 꽃이 점차 피도록
    def blomming_flower(self) :
        self.cur += self.steps
        StepCounter = 0
        
        StepPins = StepPins_open
        for _ in range(self.steps) :
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

    # 꽃 제자리로
    def close_flower(self) :
        StepCounter = 0
        
        StepPins = StepPins_close
        for _ in range(self.cur) :
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
        
        self.cur = 0
        

