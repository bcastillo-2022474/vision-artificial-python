import cv2
import numpy as np
import serial

COM = 'COM4'    
BAUD = 9600
ser = serial.Serial(COM, BAUD)
MAX_CAMERA_WIDTH_RESOLUTION = 614
MAX_CAMERA_HEIGHT_RESOLUTION = 420
MAX_HORIZONTAL_POSSIBLE_DEGREES = 180
MAX_VERTICAL_POSSIBLE_DEGREES = 90
STEPS = 5

cap = cv2.VideoCapture(0)
azulBajo = np.array([160, 100, 20], np.uint8)
azulAlto = np.array([180, 255, 255], np.uint8)
last_height_degrees = 0
last_width_degrees = 0
while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(frameHSV, azulBajo, azulAlto)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contornos, -1, (255, 0, 0), 4)

        for c in contornos:
            # print("WTFFFFFFF", last_height_degrees, last_width_degrees)
            area = cv2.contourArea(c)
            if area > 6000:
                M = cv2.moments(c)
                if M["m00"] == 0:
                    M["m00"] = 1
                x = int(M["m10"] / M["m00"])
                y = int(M['m01'] / M['m00'])
                cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)

                current_width_degrees = min(round(round((x*MAX_HORIZONTAL_POSSIBLE_DEGREES)/MAX_CAMERA_WIDTH_RESOLUTION)/STEPS)*STEPS, MAX_HORIZONTAL_POSSIBLE_DEGREES)
                current_height_degrees = min(round(round((y*MAX_VERTICAL_POSSIBLE_DEGREES)/MAX_CAMERA_HEIGHT_RESOLUTION)/STEPS)*STEPS,MAX_VERTICAL_POSSIBLE_DEGREES) 

                if (last_height_degrees == current_height_degrees) and (last_width_degrees == current_width_degrees):
                    # print("NO SE DEBERIA MOVER")
                    continue

                print("EJE X: ")
                print(last_width_degrees, current_width_degrees, last_width_degrees == current_width_degrees)
                print("EJE Y: ")
                print(last_height_degrees, current_height_degrees, last_height_degrees == current_height_degrees)
                
                last_height_degrees = current_height_degrees
                last_width_degrees = current_width_degrees
                print("Moviendo a la posicion: ", current_width_degrees, current_height_degrees)
                ser.write((str(last_height_degrees) + "@" + str(last_width_degrees) + "#").encode())

        # cv2.imshow('mascaraAzul', mascara)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            ser.close()
            break
cap.release()
cv2.destroyAllWindows()