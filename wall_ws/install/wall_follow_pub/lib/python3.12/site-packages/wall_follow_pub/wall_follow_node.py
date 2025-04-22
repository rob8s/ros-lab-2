import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class WallFollower(Node):
    def __init__(self):
        super().__init__('wall_follower')
        self.publisher_ = self.create_publisher(Twist, 'diff_drive/cmd_vel', 10)
        self.subscription_ = self.create_subscription(LaserScan, '/diff_drive/scan', self.movement_callback, 10)

        # Placeholders
        self.left_follow_dist = 1.5
        self.integral = 0
        self.prev_error = 0
        self.dt = 0.1
        self.kp = 0.1
        self.ki = 0.0
        self.kd = 0.6

    def movement_callback(self, msg):
        front = msg.ranges[0]
        left = msg.ranges[1]
        cmd = Twist()

        error = left - self.left_follow_dist
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        change = self.kp * error + self.ki * self.integral + self.kd * derivative
        
        cmd.linear.x = 1.0
        cmd.angular.z = change

        if front < 1.8:
            # Wall directly in front → turn away immediately
            cmd.linear.x = 0.2
            cmd.angular.z = -1.0
        elif left > 2:
            cmd.linear.x = 0.5
            cmd.angular.z = 0.5

        self.prev_error = error
        self.publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = WallFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
