# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 09:24:59 2020

@author: santi
"""
#--------------------------------------------------------------------------
#------- Analisis-------------------------------------------
#------- Por: Santiago Alvarez Pinzon    santiago.alvarezp@udea.edu.co --------------
#-------      Profesor auxiliar Universidad de Antioquia  -----------------
#-------      CC 1152463106 -------------------
#-------      Sebastian Larrea Henao    sebastian.larrea@udea.edu.co --------------
#-------      CC 1020491334 -------------------
#------- Curso Básico de Procesamiento de Imágenes y Visión Artificial-----
#------- diciembre 2020--------------------------------------------------
#-------------------------------------------------------------------------- 


import numpy as np
import cv2
from line import main
 #--------------------------------------------------------------------------
#--1. Inicializacion-----------------------------------------------
#--------------------------------------------------------------------------
#---- Se carga el video-------------------------
def prj(file):
    cap = cv2.VideoCapture(file)
    #cap = cv2.VideoCapture('recta.mp4')
    #---- Se definen los parametros de deteccion de esquinas shi-Tomasi-------------------------
    feature_params = dict( maxCorners = 100,
                           qualityLevel = 0.3,
                           minDistance = 7,
                           blockSize = 7 )
     
    #---- Parámetros para el flujo óptico de Lucas Kanade-------------------------
    lk_params = dict( winSize = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
     
    
    color = np.random.randint(0,255,(100,3))# Colores aleatorios para las trayectorias
    # Toma el primer cuadro y encuentra esquinas en él
    ret, old_frame = cap.read()# Captura de un frame para extraccion de parametros de inicio
    
    #---- Parametros para seccionado-------------------------
    
    y=465
    x=500
    h=1400
    w=2000
    cv2.imwrite("first.png", old_frame)#Muestra de imagen seccionada con las trayectorias obtenidas
    old_frame = old_frame[x:w, y:h]#Definicion de frame previo
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)#Transformacion blanco y negro de frame previo
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)#Calculo de puntos de interes para el flujo

    mask = np.zeros_like(old_frame)# máscara de imagen para dibujar las trayectorias
#--------------------------------------------------------------------------
#--2. ciclo de lectura de frames-----------------------------------------------

    
    while(1): #
      ret,frame = cap.read()#captura nuevo frame
      if not ret:
         print("hELLO ")#Condicion de , no frames disponibles
         break
      frame = frame[x:w, y:h]
      frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#Conversion a blanco y negro de frame nuevo
     
      p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params) # calcula optical flow
     
      # Select good points
      good_new = p1[st==1]#Se seleccionan los puntos para dibujar secciones de trayectorias
      good_old = p0[st==1]
#--------------------------------------------------------------------------
#--3. Creacion de mascaras ----------------------------------------------- 
      for i,(new,old) in enumerate(zip(good_new,good_old)):  # dibuja las lineas
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)#Se actualizan las trayectorias dibujando en la mascara
        frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)#Dibuja un circulo al final
      img = cv2.add(frame,mask)#Suma las imagenes para mostrar
     
      cv2.imshow('Figura1',img)#muestra la imagen obtenida
      #cv2.imshow('Figura2',mask)
    
      k = cv2.waitKey(30) #&amp; 0xff##Boton de salida
      if k == 27:
        print("bye bye")
        break
      if k == 13:
        print("Bueno eso fue un enter")
        mask = np.zeros_like(old_frame)#Reinicio de la mascara
    
      # Ahora actualiza el marco anterior y los puntos anteriores
      old_gray = frame_gray.copy()
      p0 = good_new.reshape(-1,1,2)
     #--3. Finalizacion deteccion-----------------------------------------------
      
    cv2.destroyAllWindows()#Cierre de ventanas
    cap.release()
    y=465
    x=335
    h=1400
    w=2000
    old_frame = old_frame[x:w, y:h]
    cv2.imwrite("routes.png", mask)#Muestra de imagen seccionada con las trayectorias obtenidas
    main()
