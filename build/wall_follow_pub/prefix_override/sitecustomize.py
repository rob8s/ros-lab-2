import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/batesr6/robotics/lab2/ros-lab-2/install/wall_follow_pub'
