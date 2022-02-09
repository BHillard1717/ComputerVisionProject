import math
import cv2
import mediapipe
import time
import keyboard
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

import HandTrackingModule as htm
cap = cv2.VideoCapture(0)
detectorHand = htm.handDetector(detectionCon=0.7)
pTime = 0
cTime = 0
targetPoint = 0

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[2]
volDist = volRange[2] - volRange[0]
print(volRange)
print(minVol, maxVol, volDist)
while True:
    success, img = cap.read()
    img = detectorHand.findHands(img)
    lmList = detectorHand.findPosition(img, draw=False)
    #print(lmList)
    if len(lmList) != 0:
        xThumb, yThumb = lmList[4][1], lmList[4][2]
        xIndex, yIndex = lmList[8][1], lmList[8][2]

        cv2.circle(img, (xThumb, yThumb), 15, (255, 0 ,255), cv2.FILLED)
        cv2.circle(img, (xIndex, yIndex), 15, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (xThumb,yThumb), (xIndex,yIndex), (255,0,255), 5)





    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    img = cv2.flip(img, 1)

    cv2.putText(img, str(fps.__floor__()), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)