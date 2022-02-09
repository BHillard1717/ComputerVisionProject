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
volLevel = (abs(volume.GetMasterVolumeLevel()/volDist))
freezeVolume = True
controlMode = True
while True:
    if keyboard.is_pressed(' '):
        freezeVolume = not freezeVolume
        print("Switching Mode: Take finger Off Key")
        time.sleep(1)
    elif keyboard.is_pressed('s'):
        controlMode = not controlMode
        print("Switching Mode: Take finger Off Key")
        time.sleep(1)
    success, img = cap.read()
    img = detectorHand.findHands(img)
    lmList = detectorHand.findPosition(img, draw=False)
    #print(lmList)
    if len(lmList) != 0:
        xThumb, yThumb = lmList[4][1], lmList[4][2]
        xIndex, yIndex = lmList[8][1], lmList[8][2]
        xWrist, yWrist = lmList[0][1], lmList[0][2]

        #cv2.circle(img, (xThumb, yThumb), 15, (255, 0 ,255), cv2.FILLED)
        cv2.circle(img, (xIndex, yIndex), 15, (255, 0, 255), cv2.FILLED)
        #cv2.circle(img, (xWrist, yWrist), 15, (255, 0, 255), cv2.FILLED)

        #cv2.line(img, (xThumb,yThumb), (xIndex,yIndex), (255,0,255), 5)
        #cv2.line(img, (xWrist, yWrist), (xIndex, yIndex), (255, 0, 255), 5)

        if controlMode:
            cv2.circle(img, (xThumb, yThumb), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (xThumb, yThumb), (xIndex, yIndex), (255, 0, 255), 5)
            volLength = math.hypot(xIndex - xThumb, yIndex - yThumb)
            # bounds are 20 to 200
            volLevel = (volLength - 20) / 180
        else:
            print(yIndex)
            #bounds 450 to 50
            volLevel = 1 - (yIndex - 50) / 400
        if volLevel > 1:
            volLevel = 1
        elif volLevel < 0:
            volLevel = 0
        convertedVolLevel = minVol + (volDist * volLevel)
        if convertedVolLevel == maxVol:
            convertedVolLevel = maxVol-0.1
        if not freezeVolume:
            volume.SetMasterVolumeLevel(convertedVolLevel, None)
        #cv2.putText(img, str(volLevel), (10, 300), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)





    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    img = cv2.flip(img, 1)
    cv2.rectangle(img, (50,100), (85, 400), (0,0,255), 3)
    cv2.rectangle(img, (50,400-(volLevel*100*3).__floor__()), (85, 400), (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'{int((volLevel*100).__floor__())} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.putText(img, str(fps.__floor__()), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)