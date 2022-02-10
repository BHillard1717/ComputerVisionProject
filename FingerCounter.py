import cv2
import time

import HandTrackingModule as htm
cap = cv2.VideoCapture(0)
detectorHand = htm.handDetector(detectionCon=0.7)
pTime = 0
cTime = 0
targetPoint = 0
while True:
    success, img = cap.read()
    img = detectorHand.findHands(img)
    lmList = detectorHand.findPosition(img, draw=False)
    numFingers = 0
    fingerStr = ""
    if len(lmList) != 0:
        xThumb, yThumb = lmList[4][1], lmList[4][2]
        xIndex, yIndex = lmList[8][1], lmList[8][2]

        if lmList[8][2] < lmList[6][2]:
            fingerStr = fingerStr + "Index"
            numFingers = numFingers + 1
        if lmList[12][2] < lmList[10][2]:
            fingerStr = fingerStr + "Middle"
            numFingers = numFingers + 1
        if lmList[16][2] < lmList[14][2]:
            fingerStr = fingerStr + "Ring"
            numFingers = numFingers + 1
        if lmList[20][2] < lmList[18][2]:
            fingerStr = fingerStr + "Pinky"
            numFingers = numFingers + 1
        if lmList[4][1] > lmList[8][1] and lmList[4][1] > lmList[3][2]:
            fingerStr = fingerStr + "Thumb"
            numFingers = numFingers + 1
        print(numFingers)
        print(fingerStr)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    img = cv2.flip(img, 1)

    cv2.putText(img, str(fps.__floor__()), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.putText(img, f'Number Shown: {numFingers}', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
