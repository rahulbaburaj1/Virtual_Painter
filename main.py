import cv2
import HandTrackingModule as htm
import numpy as np


cap = cv2.VideoCapture(0)
detector=htm.handDetector()
drawColor=(0,0,0)
img_canvas = np.zeros((620,1200,3),np.uint8)

while True:
    success,img = cap.read()
    img = cv2.resize(img,(1200,620))
    
    img = cv2.rectangle(img,pt1= (10,10),pt2= (240,100),color=(0,128,0),thickness=-1)
    img = cv2.rectangle(img,pt1= (250,10),pt2= (490,100),color=(0,0,128),thickness=-1)
    img = cv2.rectangle(img,pt1= (500,10),pt2= (720,100),color=(0,255,0),thickness=-1)
    img = cv2.rectangle(img,pt1= (730,10),pt2= (950,100),color=(128,0,0),thickness=-1)
    img = cv2.rectangle(img,pt1= (960,10),pt2= (1170,100),color=(255,255,255),thickness=-1)
    cv2.putText(img,text="EARASER",org=(990,60),fontFace=cv2.FONT_HERSHEY_COMPLEX,color=(0,0,0),fontScale=1,thickness=2)

    #find hands
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    #print(lmlist)
    if len(lmlist)!=0:
      x1,y1 = lmlist[8][1:]
      x2,y2 = lmlist[12][1:]
      #print(x1,y1)
  #3. check which finger is up
      fingers=detector.fingersUp()
        # print(fingers)

#4.if selection mode - two finger is up
      if fingers[1] and fingers[2]:
            xp, yp = 0,0
            #print('selection Mode')

            #checking for the click
            if y1 < 100:
                if 20 < x1 < 240:

                    drawColor = (0, 128, 0)
                elif 250 < x1 < 490:

                    drawColor = (0, 0, 128)
                elif 500 < x1 < 720:

                    drawColor = (0, 255, 0)
                elif 730 < x1 < 950:

                    drawColor = (128,0,0)
                elif 960<x1<11170:

                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1, y1 + 15), (x2, y2 + 15), drawColor, cv2.FILLED)

#5. if drawing mode - index finger is up
      if(fingers[1]and not fingers[2]):
               #print('drawing mode')
    
    
               if xp == 0 and yp ==0:
       
                 xp = x1
                 yp = y1

       
         
         
               if drawColor == (0,0,0):
     
                cv2.line(img,(xp,yp),(x1,y1),color=drawColor,thickness=50)
                cv2.line(img_canvas,(xp,yp),(x1,y1),color=drawColor,thickness=50)


               else:
                cv2.line(img,(xp,yp),(x1,y1),color=drawColor,thickness=10)
                cv2.line(img_canvas,(xp,yp),(x1,y1),color=drawColor,thickness=10)
               xp,yp = x1,y1   

    img_gray = cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)
    
    _,img_inv = cv2.threshold(img_gray,20,255,cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img,img_inv)
    img = cv2.bitwise_or(img,img_canvas)
    img = cv2.addWeighted(img,1,img_canvas,0.5,0)
    cv2.imshow('virctual_painter',img)
    
    if cv2.waitKey(1) & 0xFF==27:
            break
    
#cap.release()
#cv2.destroyAllWindows()