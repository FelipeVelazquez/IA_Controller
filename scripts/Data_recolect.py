#!/usr/bin/env python

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
import sklearn
import skimage
from skimage.transform import resize


#cap = cv2.VideoCapture(0)
#joy = xbox.Joystick()
servo = maestro.Controller()

servo.setTarget(0, 6000)
servo.setTarget(1, 6000)
topic = "/zed2/zed_node/stereo_raw/image_raw_color"

count = 0

vary = 6000

Imagen = []
Velocidad = []
Direccion = []

ser = serial.Serial('/dev/ttyACM0')

def callback(data):
	if Joy.Back() != 1:
	    #check, frame = cap.read()
	    #frame2 = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)
	    #cv2.imshow('Webcam Video', frame2)
	    bridge = CvBridge()
	    frame = bridge.imgmsg_to_cv2(data, "bgr8")

	    #data_X = joy.rigthX() # Izquierda y Derecha
	    #data_Y = joy.leftY() #Arriba y abajo o adelante y atras
	    ser.write(b'1\n')
	    data_XY = ser.readline()

	    (data_X, data_Y) = data_XY.split(',')
	    
	    gradosX = (float(data_X) * 3000) + 6000
	    servo.setTarget(0, int(gradosX))

	    gradosY = (float(data_Y) * 3000) + 6000
	    servo.setTarget(1, int(gradosY))

	    print("Grados: " + str(int(gradosY)) + " Joy: " + str(data_Y))

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
		np.save('Imagenes.npy', Imagenes)
		np.save('Velocidad.npy', Velocidad)
		np.save('Direccion.npy', Direccion)	
		Joy.close()

def listener():
	rospy.init_node('ai_dataCreator', anonymous=True)
    rospy.Subscriber(topic, Image, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()