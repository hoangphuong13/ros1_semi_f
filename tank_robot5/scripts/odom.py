#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Quaternion, Twist
import tf
import math

def odom_publisher():
    # Khởi tạo node
    rospy.init_node('odom_publisher', anonymous=True)
    pub = rospy.Publisher('/odom', Odometry, queue_size=10)
    broadcaster = tf.TransformBroadcaster()
    rate = rospy.Rate(10)  # 10 Hz

    # Khởi tạo giá trị ban đầu
    x = 0.0
    y = 0.0
    theta = 0.0
    vx = 0.1  # Vận tốc tuyến tính (m/s) - giả lập
    vth = 0.1  # Vận tốc góc (rad/s) - giả lập
    current_time = rospy.Time.now()
    last_time = rospy.Time.now()

    while not rospy.is_shutdown():
        current_time = rospy.Time.now()

        # Tính toán vị trí mới (giả lập chuyển động)
        dt = (current_time - last_time).to_sec()
        delta_x = vx * math.cos(theta) * dt
        delta_y = vx * math.sin(theta) * dt
        delta_theta = vth * dt

        x += delta_x
        y += delta_y
        theta += delta_theta

        # Tạo quaternion từ góc theta
        odom_quat = tf.transformations.quaternion_from_euler(0, 0, theta)

        # Xuất bản TF từ odom -> base_link
        broadcaster.sendTransform(
            (x, y, 0.0),
            odom_quat,
            current_time,
            "base_link",
            "odom"
        )

        # Tạo message Odometry
        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        # Điền dữ liệu vị trí
        odom.pose.pose.position = Point(x, y, 0.0)
        odom.pose.pose.orientation = Quaternion(*odom_quat)

        # Điền dữ liệu vận tốc
        odom.twist.twist.linear.x = vx
        odom.twist.twist.angular.z = vth

        # Xuất bản topic /odom
        pub.publish(odom)

        last_time = current_time
        rate.sleep()

if __name__ == '__main__':
    try:
        odom_publisher()
    except rospy.ROSInterruptException:
        pass