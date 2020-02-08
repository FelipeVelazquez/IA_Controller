#!/usr/bin/env python

import cv2
from time import sleep
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import xbox
import maestro 


cap = cv2.VideoCapture(0)
joy = xbox.Joystick()
servo = maestro.Controller()

inputCommand = 0
saveQ = 0
name_img = 0

Derecho = ''
aint = 0

Atras = ''
atint = 0

Izquierda = ''
izint = 0

Derecha = ''
derint = 0

data_X = 0.0
data_y = 0.0

Giro = 0.0

servo.setTarget(0, 6000)
servo.setTarget(1, 6000)


while True:
    check, frame = cap.read()
    frame2 = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)
    cv2.imshow('Webcam Video', frame2)

    data_X = joy.leftX() # Izquierda y Derecha
    data_Y = joy.leftY() #Arriba y abajo o adelante y atras
    servo.setTarget(1, 6000)

    if data_X >= 0.5:
    	aint = aint + 1
    	Derecho = 'Derecho/derecho' + str(aint) + '.jpg'
    	cv2.imwrite(filename=Derecho, img=frame2)
    	print('Guardando Adelante: ' + str(aint))
    	servo.setTarget(1, 6100)
        
    elif data_X <= -0.5: # press Q for save image has Coca-cola
        atint = atint + 1
    	Atras = 'Atras/atras' + str(atint) + '.jpg'
    	cv2.imwrite(filename=Atras, img=frame2)
    	print('Guardando Atras: ' + str(atint))
    	servo.setTarget(1, 5900)

    elif data_Y >= 0.5: # press W for save image has termo
        izint = izint + 1
    	Izquierda = 'Izquierda/izuierda' + str(izint) + '.jpg'
    	cv2.imwrite(filename=Izquierda, img=frame2)
    	print('Guardando Izquierda: ' + str(izint))
    	Giro = Giro - izint * 10
    	servo.setTarget(0, 6000 - Giro)

    elif data_Y <= -0.5: # press E for save image has agua
        derint = derint + 1
    	Derecha = 'Derecha/derecha' + str(derint) + '.jpg'
    	cv2.imwrite(filename=Derecha, img=frame2)
    	print('Guardando Derecha: ' + str(derint))
    	Giro = Giro + izint * 10
    	servo.setTarget(0, 6000 + Giro)