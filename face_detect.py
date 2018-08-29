import cv2
import math
import sys
import csv

# Opens a file (txt & csv)
file = open("test.txt", "w")
print file
c = csv.writer(open("test.csv", "wb"))

# Creates the haar cascade
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Assigns perameters
film = sys.argv[1]
numberOfImages = sys.argv[2]
fileExtension = sys.argv[3]

# Initializers
lowestPercentList = []

# Creates column headers for csv file
c.writerow(["  ",film.upper(),"  "])
c.writerow(["  ","  ","  "])
c.writerow(["Image Name","Pixel Distance","Percent"])

# Iterates through image groups
for i in range(1, int(numberOfImages) + 1):

    imagePath2 = str(film) + "_" + str(i) + "." + fileExtension
    file.write(imagePath2 + "\n")

    # Reads the image
    image = cv2.imread(imagePath2)
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detects faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    # Draws vertical third lines
    height, width = image.shape[:2]
    leftVertTop = ((width/3), 0)
    leftVertBtm = ((width/3), height)
    rightVertTop = (((2*width)/3), 0)
    rightVertBtm = (((2*width)/3), height)
    leftVerticalThird = cv2.line(image, leftVertTop, leftVertBtm, (0,255, 0), 1)
    rightVerticalThird = cv2.line(image, rightVertTop, rightVertBtm, (0,255, 0), 1)

    # Draws horizontal third lines
    leftHorzTop = (0, (height/3))
    rightHorzTop = (width, (height/3))
    leftHorzBtm = (0, ((2*height)/3))
    rightHorzBtm = (width, ((2*height)/3))
    topHorizontalThird = cv2.line(image, leftHorzTop, rightHorzTop, (0, 255, 0), 1)
    bottomHorizontalThird = cv2.line(image, leftHorzBtm, rightHorzBtm, (0 ,255, 0), 1)

    # Values of the third lines
    leftVertX = width/3
    rightVertX = (2*width)/3
    topHorzY = height/3
    btmHorzY = (2*height)/3

    # Initializers 
    j = 1
    rectangleAreaList = []
    distanceFromPowerPointList = []
    percentList = []

    # Draws a rectangle around the faces, line at the eye line, and an approximated facial focal point
    for (x, y, w, h) in faces:
        faceRectagle = cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        rectangleArea = w*h
        eyeLine = cv2.line(image, (x, y+(h/3)), (x+w, y+(h/3)), (0, 0, 255), 1)
        focalPointX = x+(w/2)
        focalPointY = y+(h/3)
        focalPoint = cv2.circle(image, (focalPointX, focalPointY), 2, (0, 0, 255), 2)

        # Finds distance between focal points and third lines
        distanceLeftVert = abs(focalPointX - leftVertX)
        distanceRightVert = abs(focalPointX - rightVertX)
        distanceTopHorz = abs(focalPointY - topHorzY)
        distanceBtmHorz = abs(focalPointY- btmHorzY)

        # Determines closest power point 
        if distanceLeftVert < distanceRightVert:
            powerPointX = width/3
        else:
            powerPointX = (2*width)/3
            
        if distanceTopHorz < distanceBtmHorz:
            powerPointY = height/3
        else:
            powerPointY = (2*height)/3

        # Finds distance from focal point to closest power point
        distanceFromPowerPoint = abs(math.sqrt((powerPointX - focalPointX)**2 + (powerPointY - focalPointY)**2 ))

        # Finds the x and y value in each quadrant furthest from the each respective power point
        if focalPointX < leftVertX:
            farthestPointX = 0
        elif focalPointX > rightVertX:
            farthestPointX = width
        else:
            farthestPointX = width/2

        if focalPointY < topHorzY:
            farthestPointY = 0
        elif focalPointY > btmHorzY:
            farthestPointY = height
        else:
            farthestPointY = height/2

        # Calculates percentage to show how focal point/power point proximity
        maxDistance = abs(math.sqrt((powerPointX - farthestPointX)**2 + (powerPointY - farthestPointY)**2 ))
        normalizedPercent = distanceFromPowerPoint / maxDistance * 100

        # Prints results
        dataLine = "  " + str(j) + "\t\t"+ str((focalPointX, focalPointY)) + "\t\t"+ str(round(distanceFromPowerPoint, 1)) + "\t\t" + str(rectangleArea) + "\t\t" + str(round(normalizedPercent, 1)) + "%"
        file.write(dataLine + "\n")

        # Finds biggest faces/focal point
        rectangleAreaList.append(rectangleArea)
        distanceFromPowerPointList.append(distanceFromPowerPoint)

        percentList.append(normalizedPercent)
        lowestPercentList.append(min(percentList))
                
        j = j+1

    # Prints final results for biggest face (txt & csv)
    finalResults2 = "Face number: " + str(distanceFromPowerPointList.index(min(distanceFromPowerPointList)) + 1) + "\t\t" + "Distance: " + str(round(min(distanceFromPowerPointList))) +  "\t\t" + "Percent: " + str(round(min(percentList), 1)) + "\n\n\n\n"
    file.write(finalResults2)
    c.writerow([imagePath2,round(min(distanceFromPowerPointList)),round(min(percentList), 1)])

    i = i + 1

average = sum(lowestPercentList) / float(len(lowestPercentList))
file.write("Average percent" + "\t\t" + str(round(average, 1)) + "%" + "\n\n\n\n")
file.close()

c.writerow([])
c.writerow(["Average Percent:"," ",str(round(average, 1)) + "%"])

cv2.imshow(imagePath2, image)
#cv2.waitKey(0)
cv2.waitKey(5000)
cv2.destroyAllWindows()

