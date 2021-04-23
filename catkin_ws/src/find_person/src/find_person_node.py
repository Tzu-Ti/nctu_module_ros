#!/usr/bin/python
import rospy
from std_msgs.msg import Int32, Bool, String

import time

class Find_person(object):
	def __init__(self):
		# Initialize
		self.X = None
		self.Y = None
		self.Bottom = None

		self.noneCount = 0

		# Publishers
		self.pub_camera = rospy.Publisher("~exe_camera", Bool, queue_size=1)
		self.pub_control = rospy.Publisher("~find_control", String, queue_size=1)
	
		# Subscribers
		# 12/02
		# self.sub_exe_find = rospy.Subscriber("~exe_find", Bool, self.start, queue_size=1)
		self.sub_location = rospy.Subscriber("~location", String, self.locate, queue_size=1)
		self.start()
	
	def locate(self, location_msg):
		location_msg = location_msg.data
		print("[find_person_node] locate", location_msg)
		if 'None' in location_msg:
			self.X = None
			self.Y = None
			self.Bottom = None
			
			self.noneCount += 1
			self.turn()
		else:
			location = location_msg.split(' ')
			self.X = float(location[0])
			self.Y = float(location[1])
			self.Bottom = float(location[2])
			self.noneCount = 0
			self.decision()

	def turn(self):
		if self.noneCount >= 2:
			print("no target in this scene")
			self.send_find_control("turn")

	def decision(self):
		X = self.X
		Y = self.Y
		area = self.Bottom
		if area > 300:
			print("Reach the target!")
		elif X > 285 and X <= 355:
			print("I should go straight")
			self.send_find_control("straight")
		elif X > 120 and X <= 285:
			print("I should turn little left")
			self.send_find_control("litleft")
		elif X > 355 and X <= 520:
			print("I should turn little right")
			self.send_find_control("litright")
		elif X <= 120:
			print("I should turn big left")
			self.send_find_control("bigleft")
		elif X > 520:
			print("I should turn big right")
			self.send_find_control("bigright")


	def start(self):
		print("[find_person_node] Start find person!!")
		time.sleep(5)
		self.send_exe_camera(True)

	def send_exe_camera(self, BOOL):
		exe_msg = Bool()
		exe_msg.data = BOOL
		print("Publishing")
		self.pub_camera.publish(exe_msg)

	def send_find_control(self, cmd):
		control_msg = String()
		control_msg.data = cmd
		self.pub_control.publish(control_msg)

if __name__ == "__main__":
	rospy.init_node("find_person", anonymous=False)
	find_person = Find_person()
	rospy.spin()
