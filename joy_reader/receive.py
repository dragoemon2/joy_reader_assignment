import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from geometry_msgs.msg import Twist


SPEED_COEFFICIENT = 1.0
ROTATE_SPEED_COEFFICIENT = 1.0

class JoyReader(Node):
    def __init__(self):
        super().__init__('joy_reader')

        self.subscriber = self.create_subscription(
            Joy,
            "/joy",
            self.read_event,
            10
        )

        self.publisher = self.create_publisher(
            Twist,
            "robot_twist",
            10
        )

        self.print("JoyReader started")

    def read_event(self, msg:Joy):
        self.print(f"axes={repr(msg.axes)}, buttons={repr(msg.buttons)}")

        twist = Twist()

        twist.linear.x = - SPEED_COEFFICIENT * msg.axes[0]
        twist.linear.y = + SPEED_COEFFICIENT * msg.axes[1]
        twist.angular.z = ROTATE_SPEED_COEFFICIENT * msg.axes[2]

        self.publisher.publish(twist)
        
        
    def print(self, text:str):
        self.get_logger().info(text)
        


def main(args=None):
    #ros2初期化(?)
    rclpy.init(args=args)

    reader = JoyReader()

    #メインループ
    rclpy.spin(reader)

    #終了
    reader.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
