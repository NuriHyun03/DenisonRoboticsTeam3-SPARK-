import rclpy
import time
import lgpio
from rclpy.node import Node
import serial

from std_msgs.msg import String

class movement(Node):
    def __init__(self):
        super().__init__('ff_sense_movement')
        self.subscription = self.create_subscription(String, 'ir_sensors', self.sendToPico, 1)
        self.moveMotor = serial.Serial('/dev/ttyACM0')

    def sendToPico(self, msg):
        self.get_logger().info(msg.data)
        msg1 = msg.data
        msg1 = msg1.split(",")
        tur1 = msg1[0]
        irE1 = msg1[1]
        irW1 = msg1[2]
        irN1 = msg1[3]
        irS1 = msg1[4]

        if(int(tur1) == 0 or int(irE1) == 0 or int(irS1) == 0 or int(irW1) == 0 or int(irN1) == 0):
            self.get_logger().info("GOTTTTTTTHEEEEEEEMESSSAGGGGEEE")
            self.moveMotor.write(b"1\n")
            data = self.moveMotor.readline()
            print(data)

def main():
    try:
        rclpy.init()
        sub = movement()
        rclpy.spin(sub)

    except KeyboardInterrupt:
        sub.destroy_node()
        rclpy.shutdown()

main()