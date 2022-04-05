import RPi.GPIO as GPIO          
from time import sleep

# connection slots for controlling the motor driver
# numbers remains tentative until we decide which I/O slots we are using
# right motor
Rin1 = 21
Rin2 = 20
Ren = 12
# left motor
Len = 26 
Lin1 = 13
Lin2 = 19

# initial speed i.e. base duty cycle
initial_speed = 25

#  initialize motors
GPIO.setmode(GPIO.BCM)
GPIO.setup(Rin1,GPIO.OUT)
GPIO.setup(Rin2,GPIO.OUT)
GPIO.setup(Ren,GPIO.OUT)
GPIO.output(Rin1,GPIO.LOW)
GPIO.output(Rin2,GPIO.LOW)
Rp=GPIO.PWM(Ren,50)
GPIO.setup(Lin1,GPIO.OUT)
GPIO.setup(Lin2,GPIO.OUT)
GPIO.setup(Len,GPIO.OUT)
GPIO.output(Lin1,GPIO.LOW)
GPIO.output(Lin2,GPIO.LOW)
Lp=GPIO.PWM(Len,50)

Rp.start(initial_speed)
Lp.start(initial_speed)

class move():

    def stop(self):
        GPIO.output(Rin1,GPIO.LOW)
        GPIO.output(Rin2,GPIO.LOW)
        GPIO.output(Lin1,GPIO.LOW)
        GPIO.output(Lin2,GPIO.LOW)

    def low_speed(self):
        Rp.ChangeDutyCycle(25)
        Lp.ChangeDutyCycle(25)

    def med_speed(self):
        Rp.ChangeDutyCycle(50)
        Lp.ChangeDutyCycle(50)
    
    def high_speed(self):
        Rp.ChangeDutyCycle(75)
        Lp.ChangeDutyCycle(75)

    def forward(self):
        GPIO.output(Rin2,GPIO.LOW)
        GPIO.output(Rin1,GPIO.HIGH)
        GPIO.output(Lin1,GPIO.LOW)
        GPIO.output(Lin2,GPIO.HIGH)
        
    def reverse(self):
        GPIO.output(Rin1,GPIO.LOW)
        GPIO.output(Rin2,GPIO.HIGH)
        GPIO.output(Lin1,GPIO.HIGH)
        GPIO.output(Lin2,GPIO.LOW) 
        
    def escape():
        GPIO.cleanup()
