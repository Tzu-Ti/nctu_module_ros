import cv2
import picamera
import numpy as np
import time
import socket

class Yolo(object):
	def __init__(self, target):
                ##### Socket #####
                ### GPU computer ###
                self.HOST = "192.168.0.177"
                self.PORT = 5050
		
		self.target = target

	def connect(self):
		with picamera.PiCamera() as camera:
                        camera.resolution = (640, 480)
                        camera.framerate = 24
                        time.sleep(1)

			### Connect to GPU computer ###
	                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        	        s.connect((self.HOST, self.PORT))

                	s.sendall(self.target)

	
			while True:
                        	### Take a picture ###
                        	image = np.empty((480 * 640 *3,), dtype=np.uint8)
                        	camera.capture(image, format='bgr')
                        	image = image.reshape((480, 640, 3))
                        	cv2.imwrite("test.jpg", image)

				### Send image to GPU computer ###
                		imgFile = open("test.jpg")
                		while True:
					imgData = imgFile.readline(1024)
                        		if not imgData:
						s.send("over")
                                		break
					s.send(imgData)
				imgFile.close()
                		print("transit end")

				### Receive output from server ###
				location = s.recv(1024)
				print(location)

			s.close()


if __name__ == "__main__":
	# target = raw_input("Input your target: ")
	target = "orange"
	yolo = Yolo(target)
	yolo.connect()


