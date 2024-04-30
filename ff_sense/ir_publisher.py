import rclpy
from rclpy.node import Node
import time
import lgpio
import serial
from std_msgs.msg import String

handle = lgpio.gpiochip_open(0)
#lgpio.group_claim_output(handle, [5, 6, 19, 26])
lgpio.group_claim_input(handle, [3, 16, 17, 20, 21])
#lgpio.gpio_claim_input(handle, 13)
#lgpio.tx_pwm(handle, 13, 1000, 100)

class IRPublisher(Node):
    def __init__ (self):
        super().__init__('ff_sense_ir_publisher')
        self.message_counter = 0
        self.secondary_message_counter = 0
        self.sensor_publisher = self.create_publisher(String, 'ir_sensors', 10)
        self.moveMotor = serial.Serial('/dev/ttyACM0')
       #self.secondary_chatter_publisher = self.create_publisher(String, 'chatter', 10)
        #self.initialize_timers()

    def send_sensors(self):
        msg = String()
        IRTurret = lgpio.gpio_read(handle, 21)
        IREast = lgpio.gpio_read(handle, 3)
        IRWest = lgpio.gpio_read(handle, 16)
        IRNorth = lgpio.gpio_read(handle, 17)
        IRSouth = lgpio.gpio_read(handle, 20)

        msg.data = f"{IRTurret}, {IREast}, {IRWest}, {IRNorth}, {IRSouth}"
        self.sensor_publisher.publish(msg)

        if(IRTurret == 0 or IREast == 0 or IRSouth == 0 or IRWest == 0 or IRNorth == 0):
            self.get_logger().info("GOTTTTTTTHEEEEEEEMESSSAGGGGEEE")
            self.moveMotor.write(b"1\n")

        #msg = String()
        #msg.data = f'This is message number {self.message_counter}'
        #self.chatter_publisher.publish(msg)
        #self.get_logger().info(f'This is message number {self.message_counter}')
        #self.message_counter += 1
    
    '''
    def send_chatter_secondary(self):
        msg = String()
        msg.data = f'Secondary message number {self.secondary_message_counter}'
        self.chatter_publisher.publish(msg)
        self.get_logger().info(f'Publishing secondary message number {self.secondary_message_counter}')
        self.secondary_message_counter += 1
    
    def initialize_timers(self):
        self.publish_delay_primary = 0.1
        self.timer1 = self.create_timer(self.publish_delay_primary, self.send_sensors)

        self.publish_delay_secondary = 1.2
        self.timer2 = self.create_timer(self.publish_delay_secondary, self.send_chatter_secondary)
'''
def main():
    print('Hi from ff_sense.')
    try:
        rclpy.init()
        pub = IRPublisher()
        #rclpy.spin(pub)

        
        while True:
            pub.send_sensors()
            #pub.servoTest()
            #time.sleep(0.001)
        
    except KeyboardInterrupt:
        pub.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
