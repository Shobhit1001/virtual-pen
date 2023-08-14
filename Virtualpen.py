import cv2
import numpy as np
img = cv2.VideoCapture(1)

img.set(3,640)
img.set(4,480)
img.set(10,150)

#list of colors
mycolors=[
          [126,69,174,179,255,255]]
myclrvalues=[[255, 192, 203]]
mypoints=[]  #[x y colorid]

def findcolor(img, mycolors , myclrvalues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0;
    nnewpoints=[]
    for color in mycolors:
      lower = np.array(color[0:3])
      upper = np.array(color[3:6])
      mask = cv2.inRange(imgHSV, lower, upper)
      x,y=getContours(mask)
      cv2.circle(imgresult,(x,y),10,myclrvalues[count],cv2.FILLED)
      if x!=0 and y!=0:
          nnewpoints.append([x,y,count])
      count+=1
      #cv2.imshow(str(color[0]),mask)
    return nnewpoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>1000:
            #cv2.drawContours(imgresult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawoncanvas(mypoints, myclrvalues):
    for points in mypoints:
        cv2.circle(imgresult, (points[0],points[1]) , 10 ,myclrvalues[points[2]] ,cv2.FILLED)

while True:
    success, imgg = img.read()
    imgresult = imgg.copy()

    newpoints=findcolor(imgg, mycolors, myclrvalues)
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(mypoints)!=0:
        drawoncanvas(mypoints, myclrvalues)

    cv2.imshow("video", imgresult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
