# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 11:22:56 2020

@author: santi
"""
import sys
import math
import cv2 as cv
import numpy as np
#--------------------------------------------------------------------------
 #--4. Inicio procesamiento-----------------------------------------------
#--------------------------------------------------------------------------
def main():
    rho1=0#Acumulador de longitudes
    theta1=0#Acumulador de angulos
    src = cv.imread('routes.png')#Carga de la imagen   
    dst = cv.Canny(src, 50, 200, None, 3)#Delineado de la imagen
    
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)#Transformacion a color
    cdstP = np.copy(cdst)


    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)#Calculo de las lineas rectas en la imagen
    #print(lines)
#--------------------------------------------------------------------------
 #--5. Calculo y obtencion de las lineas en coordenadas caresianas-----------------------------------------------
#--------------------------------------------------------------------------
    if lines is not None:#Ciclo para recorrer cada linea
        for i in range(0, len(lines)):
            rho = lines[i][0][0] #rho en la iteracion
            theta = lines[i][0][1]#theta en la iteracion
            rho1+=rho#acumulador de rho
            theta1+=theta#acumulador de theta
            #Calculo de puntos para trazar la linea graficamente
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            #Trazado de las lineas detectadas
            #pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))#Punto 1
            #pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))#Punto 2
            #cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
    #Se encuentra la linea promedio para definir la trayectoria unificada
    rho1=rho1/len(lines)
    theta1=theta1/len(lines)
    print(rho1, theta1)
    #Calculo de puntos para trazar la linea de trayectoria unificada graficamente 
    a1 = math.cos(theta1)
    b1 = math.sin(theta1)
    x01 = a1 * rho1
    y01 = b1 * rho1
    #Trazado de la trayectoria unificada
    pt11 = (int(x01 + 1000*(-b1)), int(y01 + 1000*(a1)))#Punto 1
    pt21 = (int(x01 - 1000*(-b1)), int(y01 - 1000*(a1)))#Punto 2
    cv.line(cdst, pt11, pt21, (0,255,0), 3, cv.LINE_AA)#Dibujo de linea
    
    if(rho1<=100 and theta1>=1.57):
        print("Trayectoria ilegal")
    elif(rho1>=100 and theta1>=1.57):
        print("Giro legal")
    else: 
        print("Recta")
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)#Calculo lineas probabilisticas
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]#Se lee las lineas obtenidas
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)#Se trazan las lineas probabilisticas
    
    #cv.imshow("Source", src)#Se muestra la original
    #cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)#Se muestran lineas de transformada estandar
    #cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)#se muestran lineas de transformada probabilistica
    cv.imwrite("output.png", cdst)
    #cv.waitKey(0)#Espera de tecla para el cierre
    cv.destroyAllWindows()

    return 0
