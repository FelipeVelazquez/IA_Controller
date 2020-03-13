#!/usr/bin/env python
from __futere__ import print_function
import cv2
from time import sleep
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
#import xbox
import serial
import maestro
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError



#cap = cv2.VideoCapture(0)
#joy = xbox.Joystick()
topic = "/zed2/zed_node/right_raw/image_raw_color"

count = 0

vary = 6000

Imagen = []
Velocidad = []
Direccion = []

ser = serial.Serial('/dev/ttyACM0', baudrate = 115200)

def callback(data):
	global vary
	global count
	global Imagen
	global Velocidad
	global Direccion
	ser.write(b'1\n')
	print("Coneccion...")
	data_XYB = ser.readline()
	(data_X, data_Y, B_button) = data_XYB.split(',')
	print(data_XYB)

	try:
		bridge = CvBridge()
		cv_image = bridge.imgmsg_to_cv2(ata, "bgr8")
		cv2.imshow("Imagen Ventana", cv_image)
		cv2.waitKey(3)
	except CvBridgeError as e:
		print(e)

	if data_Y >= 0.2:
		vary = 6150
	elif data_Y < 0:
		vary = 5850
	else:
		vary = 6000

	count = count + 1

	if count >= 10 and (data_Y != 0 or data_X != 0):
		rez_img = skimage.transform.resize(frame, (150, 150, 3),mode='constant',anti_aliasing=True)
		img_arr = np.asarray(rez_img)
		Imagen.append(img_arr)
		Velocidad.append(gradosY)
		Direccion.append(gradosX)
		count = 0
	else:
		Imagen = np.asarray(Imagen)
		Velocidad = np.asarray(Velocidad)
		Direccion = np.asarray(Direccion)
		"""np.save('Imagenes.npy', Imagenes)
		np.save('Velocidad.npy', Velocidad)
		np.save('Direccion.npy', Direccion)	"""

def listener():
	rospy.init_node('ai_dataCreator', anonymous=True)
	rospy.Subscriber(topic, Image, callback)
	rospy.spin()


if __name__ == '__main__':
 	listener()