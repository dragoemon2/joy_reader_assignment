import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose

from math import cos, sin

class Simulator(Node):
    def __init__(self):
        super().__init__('simulator')
        
        self.create_subscription(
            Twist,
            'robot_twist',
            self.on_receive,
            10
        )

        self.interval = 0.01  # seconds
        self.timer = self.create_timer(self.interval, self.loop)

        self.pose = Pose()
        self.speed = Twist()

    def on_receive(self, twist:Twist):
        #あとで1次遅れにする
        self.speed = twist

    def loop(self):
        self.pose.position.x += self.interval * self.speed.linear.x * cos(self.pose.orientation.z) - self.speed.linear.y * sin(self.pose.orientation.z)
        self.pose.position.y += self.interval * self.speed.linear.x * sin(self.pose.orientation.z) + self.speed.linear.y * cos(self.pose.orientation.z)
        self.pose.orientation.z += self.interval * self.speed.angular.z

        self.print(f"{self.pose.position.x}, {self.pose.position.y}, {self.pose.orientation.z}")

    def print(self, text:str):
        self.get_logger().info(text)        

        


def main(args=None):
    #ros2初期化(?)
    rclpy.init(args=args)

    simulator = Simulator()

    #メインループ
    rclpy.spin(simulator)

    #終了
    simulator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
