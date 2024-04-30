import rclpy
import time
import lgpio
from rclpy.node import Node

from std_msgs.msg import String

handle = lgpio.gpiochip_open(0)
#lgpio.group_claim_input(handle, [3, 16, 17, 20])
lgpio.group_claim_output(handle, [5, 6, 19, 26])
#lgpio.tx_pwm(handle, 13, 50, 50)

class motorMovement(Node):
    def __init__(self):
        super().__init__('ff_sense_Msub')
        self.subscription = self.create_subscription(String, 'turret_motor', self.moveTurret, 1)
        self.fire_publisher = self.create_publisher(String, 'fire_detected', 10)
        self.numsteps = 0
        #self.subscription2 = self.create_subscription(String, 'ir_sensors', self.moveTurret, 10)

    def moveTurret(self, message1):
        self.get_logger().info(message1.data)
        if (message1.data == "Fire Detected"):
            message1.data = "Fire Detected"
            self.fire_publisher.publish(message1)
            time.sleep(10)
            return
        msg1 = message1.data
        msg1 = msg1.split(",")
        steps = msg1[0]
        motor_direction = msg1[1]
        #print(steps, motor_direction)
        if(int(steps) == 0 and int(motor_direction) == 0):
            self.get_logger().info("Got Home message")
            self.home()
            return
        i = 0
        while (i < int(steps)):
            
            #print(motor_direction)
            if (int(motor_direction) == 1):
                print('motor running clockwise')
                lgpio.gpio_write(handle, 5, 1)
                lgpio.gpio_write(handle, 6, 0)
                lgpio.gpio_write(handle, 19, 0)
                lgpio.gpio_write(handle, 26, 1)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 1)
                lgpio.gpio_write(handle, 6, 1)
                lgpio.gpio_write(handle, 19, 0)
                lgpio.gpio_write(handle, 26, 0)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 0)
                lgpio.gpio_write(handle, 6, 1)
                lgpio.gpio_write(handle, 19, 1)
                lgpio.gpio_write(handle, 26, 0)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 0)
                lgpio.gpio_write(handle, 6, 0)
                lgpio.gpio_write(handle, 19, 1)
                lgpio.gpio_write(handle, 26, 1)
                time.sleep(0.005)

                '''
                if self.lockIn(int(tur1)) == 1:
                    break
                '''
                i = i + 1
                self.numsteps = self.numsteps + 1

            elif (int(motor_direction) == 0):
                print('motor running counterclockwise')
                lgpio.gpio_write(handle, 5, 1)
                lgpio.gpio_write(handle, 6, 0)
                lgpio.gpio_write(handle, 19, 0)
                lgpio.gpio_write(handle, 26, 1)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 0)
                lgpio.gpio_write(handle, 6, 0)
                lgpio.gpio_write(handle, 19, 1)
                lgpio.gpio_write(handle, 26, 1)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 0)
                lgpio.gpio_write(handle, 6, 1)
                lgpio.gpio_write(handle, 19, 1)
                lgpio.gpio_write(handle, 26, 0)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 1)
                lgpio.gpio_write(handle, 6, 1)
                lgpio.gpio_write(handle, 19, 0)
                lgpio.gpio_write(handle, 26, 0)
                time.sleep(0.005)
                '''
                if self.lockIn(int(tur1)) == 1:
                    break
                '''
                i = i + 1
                self.numsteps = self.numsteps - 1
    
    def home(self):
        self.get_logger().info(f"Homing: {self.numsteps}")
        while(self.numsteps != 0):
            if (self.numsteps > 0):
                print('motor running counterclockwise')
                lgpio.gpio_write(handle, 5, 1)
                lgpio.gpio_write(handle, 6, 0)
                lgpio.gpio_write(handle, 19, 0)
                lgpio.gpio_write(handle, 26, 1)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 0)
                lgpio.gpio_write(handle, 6, 0)
                lgpio.gpio_write(handle, 19, 1)
                lgpio.gpio_write(handle, 26, 1)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 0)
                lgpio.gpio_write(handle, 6, 1)
                lgpio.gpio_write(handle, 19, 1)
                lgpio.gpio_write(handle, 26, 0)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 1)
                lgpio.gpio_write(handle, 6, 1)
                lgpio.gpio_write(handle, 19, 0)
                lgpio.gpio_write(handle, 26, 0)
                time.sleep(0.005)

                self.numsteps = self.numsteps - 1
            elif (self.numsteps < 0):
                print('motor running clockwise')
                lgpio.gpio_write(handle, 5, 1)
                lgpio.gpio_write(handle, 6, 0)
                lgpio.gpio_write(handle, 19, 0)
                lgpio.gpio_write(handle, 26, 1)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 1)
                lgpio.gpio_write(handle, 6, 1)
                lgpio.gpio_write(handle, 19, 0)
                lgpio.gpio_write(handle, 26, 0)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 0)
                lgpio.gpio_write(handle, 6, 1)
                lgpio.gpio_write(handle, 19, 1)
                lgpio.gpio_write(handle, 26, 0)
                time.sleep(0.005)

                lgpio.gpio_write(handle, 5, 0)
                lgpio.gpio_write(handle, 6, 0)
                lgpio.gpio_write(handle, 19, 1)
                lgpio.gpio_write(handle, 26, 1)
                time.sleep(0.005)
                self.numsteps = self.numsteps + 1

def lockIn(tur1):
    #If turret is high then stop moving
    if tur1 == 0:
        print("FIRE DETECTED!")
        return 1
    else:
        return 0

def main():
    try:
        rclpy.init()
        sub = motorMovement()
        rclpy.spin(sub)

    except KeyboardInterrupt:
        sub.destroy_node()
        rclpy.shutdown()

main()