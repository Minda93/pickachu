#!/usr/bin/env python

import cv2 
import numpy as np
import glob
import rospy

lower_black = np.array([0,0,0])
upper_black = np.array([180,255,20])
lower_white = np.array([0,0,220])
upper_white = np.array([180,255,255])

text = 'Total:'
text1 = 'Black:'
text2 = 'White:'

vid = cv2.VideoCapture(0)

vid.set(3,1280) 
vid.set(4,720) 
vid.set(5,5)
vid.set(10,0.35)

print('WIDTH',vid.get(3),'HEIGHT',vid.get(4),'FPS',vid.get(5),'BRI',vid.get(10)) 

"""def nothing(*arg):
        pass
cv2.namedWindow('edge')
cv2.createTrackbar('thrs1', 'edge', 2000, 5000, nothing)
cv2.createTrackbar('thrs2', 'edge', 4000, 5000, nothing)
"""

def Total_chess(circles, count, chessNum):
    if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
                count = count+1
                chessNum = count 
            cv2.putText(frame, text , (10, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 1, cv2.CV_AA)      
            cv2.putText(frame, str(chessNum) , (120, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 1, cv2.CV_AA)
def Black_chess(Bcircles, count, chessNum):
    if Bcircles is not None:
            Bcircles = np.uint16(np.around(Bcircles))
            for i in Bcircles[0,:]:
                # draw the outer circle
                cv2.circle(black,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(black,(i[0],i[1]),2,(0,0,255),3)
                count = count+1
                chessNum = count 
            cv2.putText(frame, text1 , (10, 150), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 1, cv2.CV_AA)      
            cv2.putText(frame, str(chessNum) , (120, 150), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 1, cv2.CV_AA) 
def White_chess(Wcircles, count, chessNum):
    if Wcircles is not None:
            Wcircles = np.uint16(np.around(Wcircles))
            for i in Wcircles[0,:]:
                # draw the outer circle
                cv2.circle(white,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(white,(i[0],i[1]),2,(0,0,255),3)
                count = count+1
                chessNum = count 
            cv2.putText(frame, text2 , (10, 250), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 1, cv2.CV_AA)      
            cv2.putText(frame, str(chessNum) , (120, 250), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 1, cv2.CV_AA)
def main():
    while(True):
        # Capture frame-by-frame
        global ret, frame, white, black
        ret, frame = vid.read() 
        cv2.circle(frame,(320,240),1,(0,0,255),-1)
        if ret == True:
            count = 0
            chessNum = 0
            img = frame.copy()
            frame = cv2.medianBlur(frame,3)
            cimg = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            black = cv2.inRange(hsv, lower_black, upper_black)
            white = cv2.inRange(hsv, lower_white, upper_white)
            circles = cv2.HoughCircles(cimg,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=60,param2=20,minRadius=10,maxRadius=20)#min = 100 max = 200  
            Bcircles = cv2.HoughCircles(black,cv2.cv.CV_HOUGH_GRADIENT,1.5,20,param1=60,param2=20,minRadius=10,maxRadius=20)#min = 100 max = 200 
            Wcircles = cv2.HoughCircles(white,cv2.cv.CV_HOUGH_GRADIENT,1.5,20,param1=60,param2=20,minRadius=10,maxRadius=20)#min = 100 max = 200 
            Total_chess(circles, count, chessNum)  
            Black_chess(Bcircles, count, chessNum) 
            White_chess(Wcircles, count, chessNum)
            cv2.imshow('ori',img)         
            cv2.imshow('detected circles',frame)
            cv2.imshow('white',white)
            cv2.imshow('black',black)


            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

        else:
            break
# Run Main
if __name__ == "__main__":
    main()
    vid.release()
    cv2.destroyAllWindows()


"""
while(True):
    # Capture frame-by-frame
    ret, frame = vid.read() 
    cv2.circle(frame,(320,240),1,(0,0,255),-1)
    if ret == True:
        count = 0
        chessNum = 0
        img = frame.copy()
        frame = cv2.medianBlur(frame,3)
        cimg = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        black = cv2.inRange(hsv, lower_black, upper_black)
        white = cv2.inRange(hsv, lower_white, upper_white)
        circles = cv2.HoughCircles(cimg,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=100,param2=30,minRadius=8,maxRadius=15)#min = 100 max = 200  
        Bcircles = cv2.HoughCircles(black,cv2.cv.CV_HOUGH_GRADIENT,1.5,20,param1=100,param2=30,minRadius=8,maxRadius=15)#min = 100 max = 200 
        Wcircles = cv2.HoughCircles(white,cv2.cv.CV_HOUGH_GRADIENT,1.5,20,param1=100,param2=30,minRadius=8,maxRadius=15)#min = 100 max = 200 
        Total_chess(circles, count, chessNum)  
        Black_chess(Bcircles, count, chessNum) 
        White_chess(Wcircles, count, chessNum)
        cv2.imshow('ori',img)         
        cv2.imshow('detected circles',frame)
        cv2.imshow('white',white)
        cv2.imshow('black',black)


        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

    else:
        break

vid.release()

cv2.destroyAllWindows()

#####################################################################


"""
