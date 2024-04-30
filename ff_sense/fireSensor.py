import time
import rclpy
from rclpy.node import Node
import serial
from std_msgs.msg import String

class fireSensor(Node):
    def __init__(self):
        super().__init__('ff_sense_fireSensor')
        self.motor_publisher = self.create_publisher(String, 'turret_motor', 10)
        self.subscription = self.create_subscription(String, 'ir_sensors', self.listener_callback, 10)
        self.moveMotor = serial.Serial('/dev/ttyACM0')
   
    def listener_callback(self, msg):
        self.get_logger().info(msg.data)
        msg1 = msg.data
        msg1 = msg1.split(",")
        tur1 = msg1[0]
        irE1 = msg1[1]
        irW1 = msg1[2]
        irN1 = msg1[3]
        irS1 = msg1[4]

        if (int(tur1) == 0):
            print("Fire Detected")
            msg.data = "Fire Detected"
            self.motor_publisher.publish(msg)
            time.sleep(0.25)
        elif(int(irS1) == 0):
            msg.data = "10, 0"
            self.motor_publisher.publish(msg)
            time.sleep(0.25)
        elif(int(irE1) == 0):
            msg.data = "10, 0"
            self.motor_publisher.publish(msg)
            time.sleep(0.25)
        elif(int(irW1) == 0):
            msg.data = "10, 1"
            self.motor_publisher.publish(msg)
            time.sleep(0.25)
        elif(int(irN1) == 0):
            msg.data = "0, 0"
            self.motor_publisher.publish(msg)
            time.sleep(0.25)
        elif(int(tur1) == 1 and int(irE1) == 1 and int(irS1) == 1 and int(irW1) == 1 and int(irN1) == 1):
            msg.data = "0, 0"
            self.motor_publisher.publish(msg)
            #self.get_logger().info("FFFFFFFFFFFFFFFFLLLLLLLLLLLLLLLAAAAAAAAAAAAGGGGGGGGGGGG")
            #self.moveMotor.write(b"0\n")
            time.sleep(0.25)

        '''
        if (int(irS1) != 1 and int(tur1) != 0):
            #numsteps, motor_direction = turnTurret(self, 300, 'c')
            msg.data = "300, 0"
            self.motor_publisher.publish(msg)
            print ("Turn Backward")
            time.sleep(10)
            #resetTurret(numsteps, motor_direction)

        elif (int(irW1) != 1 and int(tur1) != 0):
            #numsteps, motor_direction = turnTurret(self, 150, 'a')
            msg.data = "150, 1"
            self.motor_publisher.publish(msg)
            print ("Turn Left")
            time.sleep(10)
            #resetTurret(numsteps, motor_direction)
        
        elif (int(irE1) != 1 and int(tur1) != 0):
            #numsteps, motor_direction = turnTurret(self, 150, 'c')
            msg.data = "150, 0"
            self.motor_publisher.publish(msg)
            print ("Turn Right")
            time.sleep(10)
            #resetTurret(numsteps, motor_direction)
        
        elif (int(irN1) != 1 and int(tur1) != 0):
            #numsteps, motor_direction = turnTurret(self, 0, 0)
            msg.data = "0, 0"
            self.motor_publisher.publish(msg)
            print("Face Forward")
            time.sleep(10)
            #resetTurret(numsteps, motor_direction)
'''

        time.sleep(0.5)

def main():
    try:
        rclpy.init()
        sub = fireSensor()
        rclpy.spin(sub)

    except KeyboardInterrupt:
        sub.destroy_node()
        rclpy.shutdown()

main()