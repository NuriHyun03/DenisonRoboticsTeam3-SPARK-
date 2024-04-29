from machine import Pin, PWM
from picozero import DistanceSensor
from picozero import Button
import utime
import time
########################################################
# Black 12V Battery pointing FRONT
# Modify Main Loop condition with FLAME DETECTED
########################################################

flame = 0

US_Front = DistanceSensor(echo=17, trigger=16)
US_Left = DistanceSensor(echo=19, trigger=18)
US_Right = DistanceSensor(echo=20, trigger=21)
US_Back = DistanceSensor(echo=26, trigger=27)

buttonPinNo = 0
buttonPin = None
button_clicked = 0

En_AL = Pin(2, Pin.OUT) # PWM control for A
In1L = Pin(3, Pin.OUT) # control direction
In2L = Pin(4, Pin.OUT)

En_BL = Pin(6, Pin.OUT) # PWM control for B
In3L = Pin(7, Pin.OUT) # control direction
In4L = Pin(8, Pin.OUT)

En_BR = Pin(10, Pin.OUT) # PWM control for A Right
In3R = Pin(11, Pin.OUT) # control direction
In4R = Pin(12, Pin.OUT)

En_AR = Pin(13, Pin.OUT) # PWM control for B Right
In1R = Pin(14, Pin.OUT) # control direction
In2R = Pin(15, Pin.OUT)

'''
En_AL.high()
En_BL.high()
En_AR.high()
En_BR.high()
'''
pwmEn_AL = PWM(En_AL,freq=5000, duty_u16=40000)
pwmEn_BL = PWM(En_BL,freq=5000, duty_u16=40000)
pwmEn_AR = PWM(En_AR,freq=5000, duty_u16=40000)
pwmEn_BR = PWM(En_BR,freq=5000, duty_u16=40000)

def move_backward():
    '''
    In1L.high()
    In2L.low()
    In3L.high()
    In4L.low()
    In1R.high()
    In2R.low()
    In3R.high()
    In4R.low()
    '''
    In1L.high()
    In2L.low()
    In3L.high()
    In4L.low()
    In1R.high()
    In2R.low()
    In3R.high()
    In4R.low()
    print("move_backward")
    
# Backward
def move_forward():
    In1L.low()
    In2L.high()
    In3L.low()
    In4L.high()
    In1R.low()
    In2R.high()
    In3R.low()
    In4R.high()
    
#Turn Left
#Make 830ms to turn 90
def turn_left():
    In1L.low()
    In2L.high()
    In3L.low()
    In4L.high()
    In1R.high()
    In2R.low()
    In3R.high()
    In4R.low()

def turn_left_and_position():
    move_forward()
    utime.sleep_ms(500)
    stop()
    utime.sleep_ms(200)
    turn_left()
    utime.sleep_ms(830)
    stop()
    utime.sleep_ms(200)
    move_forward()
    utime.sleep_ms(700)
    
#Turn Right
#Make 830ms to turn 90
def turn_right():
    In1L.high()
    In2L.low()
    In3L.high()
    In4L.low()
    In1R.low()
    In2R.high()
    In3R.low()
    In4R.high()
   
#Stop
def stop():
    In1L.low()
    In2L.low()
    In3L.low()
    In4L.low()
    In1R.low()
    In2R.low()
    In3R.low()
    In4R.low()

def move_left():
    In1L.low()
    In2L.high()
    In3L.high()
    In4L.low()
    In1R.low()
    In2R.high()
    In3R.high()
    In4R.low()
    
def move_right():
    In1L.high()
    In2L.low()
    In3L.low()
    In4L.high()
    In1R.high()
    In2R.low()
    In3R.low()
    In4R.high()
    
def check_front_wall():
    if US_Front.value < 0.025:
        print("Front Wall Detected")
        print("Turn Requested")
        return 1
    else:
        return 0
    
def check_left_wall():
    if US_Left.value < 0.025:
        print("Left Wall Detected")
        return 1
    else:
        return 0
    
def check_right_wall():
    if US_right.value < 0.025:
        print("Right Wall Detected")
        print("Turn Requested")
        return 1
    else:
        return 0
    
def check_back_wall():
    if US_Back.value < 0.025:
        print("Back Wall Detected")
        return 1
    else:
        return 0
    
def debounceButton(pin):
    utime.sleep_ms(50)
    return pin.value()

def buttonISR(pin):
    utime.sleep_ms(50)
    if debounceButton(pin):
        "BUTTON CLICKED"
        if button_clicked == 0:
            button_clicked = 1
            stop()
            utime.sleep(1)
        if button_clicked == 1:
            button_clicked = 0
            stop()
            utime.sleep(3)
        
def setup():
    global buttonPin
    buttonPin = Pin(buttonPinNo, Pin.IN, Pin.PULL_DOWN)
    buttonPin.irq(trigger=Pin.IRQ_RISING, handler=buttonISR)
    
'''def loop():
    while True:
        while button_clicked == 0 and flame = 0:
            frontWall = check_front_wall()
            leftWall = check_left_wall()
            utime.sleep_ms(100)
            #if it detects left wall and there is nothing infront
            if frontWall == 0 and leftWall == 1:
                move_forward()
                utime.sleep_ms(500)
            #if it detects nothing
            elif frontWall == 0 and leftWall == 0:
                #turn left and position
                turn_left_and_position()
                stop()
                utime.sleep_ms(100)
                #check to see if we need to do 90 degree turn
                leftWall = check_left_wall()
                utime.sleep_ms(200)
                if leftWall == 0:
                    turn_left()
                    utime.sleep_ms(830)
                    stop()
                    utime.sleep_ms(200)
                    move_forward()
                    utime.sleep_ms(700)
                    stop()
                    utime.sleep_ms(100)
                else:
                    continue
            #if there is wall on front and left
            elif frontWall == 1 and leftWall == 1:
                #turn right 90 degree
                turn_right()
                utime.sleep_ms(830)
                stop()
                utime.sleep_ms(200)
            #if there is wall on front but not left
            elif frontWall == 1 and leftWall == 0:
                #we will not have enough space to turn left, so turn right
                turn_right()
                utime.sleep_ms(830)
                stop()
                utime.sleep_ms(200)
        #if start/stop button clicked, stop the robot until re-pressed
        while button_clicked == 1:
            stop()
            utime.sleep(1)
        #if flame detected, stop and hold the position.
        if flame == 1:
            stop()
            utime.sleep(1)
            button_clicked == 1
'''
"""def loop():
    print("moving forward")
    turn_right()
    utime.sleep_ms(850)
    stop()
    utime.sleep(5)
'''

if __name__ == "__main__":
    setup()
    loop()
"""
from machine import Pin, PWM
from picozero import DistanceSensor
from picozero import Button
import utime
import time
import sys # for reading from USB
import select
########################################################
# Black 12V Battery pointing FRONT
# Modify Main Loop condition with FLAME DETECTED
########################################################

led = Pin("LED", Pin.OUT)

flame = 0

US_Front = DistanceSensor(echo=16, trigger=17, max_distance=1)
US_Left = DistanceSensor(echo=19, trigger=18, max_distance=1)
US_Right = DistanceSensor(echo=20, trigger=21, max_distance=1)
US_Back = DistanceSensor(echo=26, trigger=27, max_distance=1)

buttonPinNo = 0
buttonPin = None
button_clicked = 0

En_AL = Pin(2, Pin.OUT) # PWM control for A
In1L = Pin(3, Pin.OUT) # control direction
In2L = Pin(4, Pin.OUT)

En_BL = Pin(6, Pin.OUT) # PWM control for B
In3L = Pin(7, Pin.OUT) # control direction
In4L = Pin(8, Pin.OUT)

En_BR = Pin(10, Pin.OUT) # PWM control for A Right
In3R = Pin(11, Pin.OUT) # control direction
In4R = Pin(12, Pin.OUT)

En_AR = Pin(13, Pin.OUT) # PWM control for B Right
In1R = Pin(14, Pin.OUT) # control direction
In2R = Pin(15, Pin.OUT)

'''
En_AL.high()
En_BL.high()
En_AR.high()
En_BR.high()
'''
pwmEn_AL = PWM(En_AL,freq=5000, duty_u16=40000)
pwmEn_BL = PWM(En_BL,freq=5000, duty_u16=40000)
pwmEn_AR = PWM(En_AR,freq=5000, duty_u16=40000)
pwmEn_BR = PWM(En_BR,freq=5000, duty_u16=40000)

def move_backward():
    '''
    In1L.high()
    In2L.low()
    In3L.high()
    In4L.low()
    In1R.high()
    In2R.low()
    In3R.high()
    In4R.low()
    '''
    In1L.high()
    In2L.low()
    In3L.high()
    In4L.low()
    In1R.high()
    In2R.low()
    In3R.high()
    In4R.low()
    print("move_forward")
    
# Backward
def move_forward():
    In1L.low()
    In2L.high()
    In3L.low()
    In4L.high()
    In1R.low()
    In2R.high()
    In3R.low()
    In4R.high()
    
#Turn Left
#Make 830ms to turn 90
def turn_left():
    In1L.low()
    In2L.high()
    In3L.low()
    In4L.high()
    In1R.high()
    In2R.low()
    In3R.high()
    In4R.low()

def turn_left_and_position():
    move_forward()
    utime.sleep_ms(500)
    stop()
    utime.sleep_ms(200)
    turn_left()
    utime.sleep_ms(830)
    stop()
    utime.sleep_ms(200)
    move_forward()
    utime.sleep_ms(700)
    
#Turn Right
#Make 830ms to turn 90
def turn_right():
    In1L.high()
    In2L.low()
    In3L.high()
    In4L.low()
    In1R.low()
    In2R.high()
    In3R.low()
    In4R.high()
   
#Stop
def stop():
    In1L.low()
    In2L.low()
    In3L.low()
    In4L.low()
    In1R.low()
    In2R.low()
    In3R.low()
    In4R.low()

def move_left():
    In1L.low()
    In2L.high()
    In3L.high()
    In4L.low()
    In1R.low()
    In2R.high()
    In3R.high()
    In4R.low()
    
def move_right():
    In1L.high()
    In2L.low()
    In3L.low()
    In4L.high()
    In1R.high()
    In2R.low()
    In3R.low()
    In4R.high()
    
def check_front_wall():
    val = US_Front.value
    if val and val < 0.25:
        print("Front Wall Detected")
        print("Turn Requested")
        return 1
    else:
        return 0
    
def check_left_wall():
    val = US_Left.value
    print(val)
    if val and val < 0.25:
        print("Left Wall Detected")
        return 1
    else:
        ("left not detected")
        return 0
        
    
def check_right_wall():
    val = US_Right.value
    if val and val < 0.25:
        print("Right Wall Detected")
        print("Turn Requested")
        return 1
    else:
        return 0
    
def check_back_wall():
    val = US_Back.value
    if val and val < 0.25:
        print("Back Wall Detected")
        return 1
    else:
        return 0
    
def debounceButton(pin):
    utime.sleep_ms(100)
    return pin.value()

def buttonISR(pin):
    global button_clicked
    utime.sleep_ms(50)
    if debounceButton(pin):
        "BUTTON CLICKED"
        if button_clicked == 0:
            button_clicked = 1
            stop()
            utime.sleep(1)
        if button_clicked == 1:
            button_clicked = 0
            stop()
            utime.sleep(3)
            
def checkFlame():
    global flame
    if select.select([sys.stdin,], [], [], 0.01)[0]:
        msg = sys.stdin.readline().strip()
        flame = int(msg)
    led.value(flame)
        
def setup():
    global buttonPin
    buttonPin = Pin(buttonPinNo, Pin.IN, Pin.PULL_DOWN)
    buttonPin.irq(trigger=Pin.IRQ_RISING, handler=buttonISR)
    
'''def loop():
    global flame
    while True:
        checkFlame()
        while button_clicked == 0 and flame == 0:
            checkFlame()
            if flame == 1:
                break
            print(f"flame: {flame}")
            print(f"button: {button_clicked}")
            frontWall = check_front_wall()
            leftWall = check_left_wall()
            utime.sleep_ms(100)
            #if it detects left wall and there is nothing infront
            if frontWall == 0 and leftWall == 1:
                move_forward()
                utime.sleep_ms(500)
            #if it detects nothing
            elif frontWall == 0 and leftWall == 0:
                #turn left and position
                turn_left_and_position()
                stop()
                utime.sleep_ms(100)
                #check to see if we need to do 90 degree turn
                leftWall = check_left_wall()
                utime.sleep_ms(200)
                if leftWall == 0:
                    turn_left()
                    utime.sleep_ms(830)
                    stop()
                    utime.sleep_ms(200)
                    move_forward()
                    utime.sleep_ms(700)
                    stop()
                    utime.sleep_ms(100)
                else:
                    continue
            #if there is wall on front and left
            elif frontWall == 1 and leftWall == 1:
                #turn right 90 degree
                turn_right()
                utime.sleep_ms(830)
                stop()
                utime.sleep_ms(200)
            #if there is wall on front but not left
            elif frontWall == 1 and leftWall == 0:
                #we will not have enough space to turn left, so turn right
                turn_right()
                utime.sleep_ms(830)
                stop()
                utime.sleep_ms(200)
        #if start/stop button clicked, stop the robot until re-pressed
        while button_clicked == 1:
            stop()
            utime.sleep(1)
        #if flame detected, stop and hold the position.
        if flame == 1:
            stop()
            utime.sleep(1)
            button_clicked == 1
'''
'''
def loop():
    print("moving forward")
    turn_right()
    utime.sleep_ms(850)
    stop()
    utime.sleep(5)
'''
def loop():
    while True:
        # Check button and flame status before entering the main logic
        if button_clicked == 0 and flame == 0:
            while True:
                # Check wall states
                frontWall = check_front_wall()
                leftWall = check_left_wall()

                utime.sleep_ms(100)

                print (leftWall)# If it detects a left wall but nothing in front
                if frontWall == 0 and leftWall == 1:
                    move_forward()
                    utime.sleep_ms(500)
                    print("moving forward")

                # If there are no walls
                elif frontWall == 0 and leftWall == 0:
                    # Turn left and position
                    turn_left_and_position()
                    stop()
                    utime.sleep_ms(100)
                    print("turning left")

                    # Recheck left wall to determine if a 90-degree turn is needed
                    leftWall = check_left_wall()
                    utime.sleep_ms(200)
                    print("left again")

                    if leftWall == 0:
                        turn_left()
                        utime.sleep_ms(830)
                        stop()
                        utime.sleep_ms(200)
                        move_forward()
                        utime.sleep_ms(700)
                        stop()
                        utime.sleep_ms(100)
                        print("left then forward")
                    else:
                        continue

                # If there are walls in front and to the left
                elif frontWall == 1 and leftWall == 1:
                    # Turn right 90 degrees
                    turn_right()
                    utime.sleep_ms(830)
                    stop()
                    utime.sleep_ms(200)
                    print("turn right cus both walls")

                # If there's a wall in front but not to the left
                elif frontWall == 1 and leftWall == 0:
                    # Turn right
                    turn_right()
                    utime.sleep_ms(830)
                    stop()
                    utime.sleep_ms(200)
                    print("turning right cus front wall")
                    
                # If button is clicked or flame is detected, exit the inner loop
                if button_clicked != 0 or flame != 0:

                    break
        else:
            # Stop the robot and wait until re-pressed
            stop()


if __name__ == "__main__":
    setup()
    loop()



# Ensure other necessary functions are defined elsewhere in the program


