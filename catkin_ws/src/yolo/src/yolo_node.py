#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32, Bool, String

import cv2
import picamera
import numpy as np
import time
import socket

class Yolo(object):
	def __init__(self):
		##### Socket #####
		### GPU computer ###
		self.HOST = "192.168.66.248"
		self.PORT = 5050

		self.yoloing = None

		# Publishers
		self.pub_location = rospy.Publisher("~location", String, queue_size=1)

		# Subscribers
		self.sub_camera = rospy.Subscriber("~exe_camera", Bool, self.camera, queue_size=1)

	##### take a picture and send to GPU computer #####
	def camera(self, exe_msg):
		target = raw_input("Input Your Target: ")
		print("[yolo_node] receive ~exe_camera")
		with picamera.PiCamera() as camera:
			camera.resolution = (640, 480)
			camera.framerate = 24
			time.sleep(1)

			### Connect to GPU computer ###
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.HOST, self.PORT))
			
			s.sendall(target)

			while not rospy.is_shutdown():	
				### Take a picture ###
				image = np.empty((480 * 640 *3,), dtype=np.uint8)
				camera.capture(image, format='bgr')
				image = image.reshape((480, 640, 3))
				cv2.imwrite("test.jpg", image)

				### Send image to GPU computer ###
				imgFile = open("test.jpg")
				while True:
					imgData = imgFile.readline(4096)
					if not imgData:
						s.send("over")
						break
					s.send(imgData)
				imgFile.close()
				print("transit end")

				### Receive yolo output from server ###
				location = s.recv(4096)
				self.send_location(location)
				time.sleep(0.3)

				if self.reach(location):
					break

			print("socket deconnection...")
			s.close()

	def send_location(self, loc):
		loc_msg = String()
		loc_msg.data = loc
		self.pub_location.publish(loc_msg)

	def reach(self, location):
		if 'None' in location:
                        X = None
                        Y = None
                        Bottom = None
                else:
                        location = location.split(' ')
                        X = float(location[0])
                        Y = float(location[1])
                        Bottom = float(location[2])
			if Bottom > 300:
				return True
                        else:
				return False

if __name__ == "__main__":
	rospy.init_node("yolo", anonymous=False)

	# target = raw_input("Input your target:")
	yolo = Yolo()
	rospy.spin()

