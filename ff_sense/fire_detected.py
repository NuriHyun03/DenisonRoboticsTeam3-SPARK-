import rclpy
import time
import lgpio
from rclpy.node import Node

from rpi_hardware_pwm import HardwarePWM

from std_msgs.msg import String

handle = lgpio.gpiochip_open(0)
lgpio.group_claim_output(handle, [23, 24])
#lgpio.group_claim_input(handle, [3, 16, 17, 20])
#lgpio.group_claim_output(handle, [5, 6, 19, 26])
lgpio.gpio_claim_input(handle, 13)
lgpio.tx_pwm(handle, 13, 1000, 100)

class fire_Detected(Node):
    def __init__(self):
        super().__init__('ff_sense_fire_detected')
        self.subscription = self.create_subscription(String, 'fire_detected', self.extinguish, 1)

    def extinguish(self, message1):
        lgpio.gpio_write(handle, 23, 1)
        lgpio.gpio_write(handle, 24, 0)
        lgpio.tx_servo(handle, 13, 2050)
        print("Pew pew")
        time.sleep(2)
        lgpio.tx_servo(handle, 13, 1950)
        time.sleep(2)
        lgpio.gpio_write(handle, 23, 0)
        lgpio.gpio_write(handle, 24, 0)
        lgpio.tx_servo(handle, 13, 2000)
        lgpio.tx_servo(handle, 13, 0)

def main():
    try:
        rclpy.init()
        sub = fire_Detected()
        rclpy.spin(sub)

    except KeyboardInterrupt:
        sub.destroy_node()
        rclpy.shutdown()

main()