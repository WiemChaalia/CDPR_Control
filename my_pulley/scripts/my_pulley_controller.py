#!/usr/bin/env python3

import rospy
from rospy import Time
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
import sys, select, tty, termios

# Set the names of the pulleys
pulley_names = ["Pulley1_Joint", "Pulley2_Joint", "Pulley3_Joint", "Pulley4_Joint"]

# Set the initial values of the pulleys
pulley_positions = [0, 0, 0, 0]

# Define the function to read the keyboard input
def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

# Initialize the ROS node
rospy.init_node('teleop_pulley')

# Initialize the joint state publisher
joint_pub = rospy.Publisher('joint_states', JointState, queue_size=10)

# Define the joint state message
joint_state = JointState()
joint_state.name = pulley_names
joint_state.position = pulley_positions
joint_state.velocity = []
joint_state.effort = []

# Set the rate of the ROS node
rate = rospy.Rate(10)

# Read the initial keyboard input settings
settings = termios.tcgetattr(sys.stdin)

# Initialize the mode to rotate all four pulleys together
mode = "all"

# Initialize the list of selected pulleys
selected_pulleys = []

while not rospy.is_shutdown():
    #asking the user
    print("""
    choose mode: 1 for individual pulleys, 2 for all pulleys, q to quit""")

    # Read the keyboard input
    key = getKey()

    # Update the mode and selected pulleys based on the keyboard input
    if key == '1':
        mode = "individual"
        selected_pulleys = []
        while len(selected_pulleys) == 0 or len(selected_pulleys) > 4:
            print("Select the pulleys to move (1-4), separated by commas:")
            pulleys_input = input()
            selected_pulleys = [int(p) for p in pulleys_input.split(',') if p.isdigit() and int(p) > 0 and int(p) <= 4]
    elif key == '2':
        mode = "all"
    elif key == 'q':
        break
    else:
        pass

    # Update the pulley positions based on the keyboard input
    if mode == "individual":
        for pulley_num in selected_pulleys:
            if pulley_num == 1:
                if key == 'w':
                    pulley_positions[0] += 0.8
                elif key == 's':
                    pulley_positions[0] -= 0.8
            elif pulley_num == 2:
                if key == 'a':
                    pulley_positions[1] += 0.8
                elif key == 'd':
                    pulley_positions[1] -= 0.8
            elif pulley_num == 3:
                if key == 'i':
                    pulley_positions[2] += 0.8
                elif key == 'k':
                    pulley_positions[2] -= 0.8
            elif pulley_num == 4:
                if key == 'j':
                    pulley_positions[3] += 0.8
                elif key == 'l':
                    pulley_positions[3] -= 0.8

    elif mode == "all":
        if key == 'w':
            for i in range(len(pulley_positions)):
                pulley_positions[i] += 0.1
        elif key == 's':
            for i in range(len(pulley_positions)):
                pulley_positions[i] -= 0.1
        else:
            pass

    # Update the joint state message
    joint_state.header.stamp = rospy.Time.now()
    joint_state.position = pulley_positions

    # Publish the joint state message
    joint_pub.publish(joint_state)

    # Sleep for the remaining time to maintain the desired rate
    rate.sleep()


