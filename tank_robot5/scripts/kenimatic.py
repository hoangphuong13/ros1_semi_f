#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

# Kích thước robot
wheel_radius = 0.05  # Bán kính bánh xe (m)
robot_width = 0.3    # Khoảng cách giữa hai bánh trái và phải (m)

# Hàm tính tốc độ bánh xe từ vận tốc tuyến tính và góc

def calculate_wheel_speeds(linear_x, angular_z):
    v_left = (linear_x - angular_z * robot_width / 2) / wheel_radius
    v_right = (linear_x + angular_z * robot_width / 2) / wheel_radius
    return v_left, v_right

# Callback xử lý lệnh vận tốc

def cmd_vel_callback(msg):
    linear_x = msg.linear.x
    angular_z = msg.angular.z

    # Tính toán tốc độ bánh xe
    left_speed, right_speed = calculate_wheel_speeds(linear_x, angular_z)

    # Xuất tốc độ bánh xe
    left_wheel_pub.publish(left_speed)
    right_wheel_pub.publish(right_speed)

if __name__ == '__main__':
    rospy.init_node('four_wheel_drive_controller')

    # Subscriber nhận lệnh vận tốc
    rospy.Subscriber('/cmd_vel', Twist, cmd_vel_callback)

    # Publisher điều khiển tốc độ bánh xe
    left_wheel_pub = rospy.Publisher('/left_wheel_speed', Float32, queue_size=10)
    right_wheel_pub = rospy.Publisher('/right_wheel_speed', Float32, queue_size=10)

    rospy.loginfo("Four-wheel robot controller started")

    rospy.spin()
