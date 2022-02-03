import cv2
import mediapipe
import time
import keyboard

import HandTrackingModule as htm
import PoseEstimationModule as pem

cap = cv2.VideoCapture(0)
detectorHand = htm.handDetector()
detectorPose = pem.poseDetector()

pTime = 0
cTime = 0
detectHand = True
detectPose = True
targetPoint = 0

while True:
    if keyboard.is_pressed('q'):
        exit(0)
    elif keyboard.is_pressed(' '):
        detectHand = not detectHand
        detectPose = not detectPose
        print("Switching Mode: Take finger Off Key")
        time.sleep(1)
    elif keyboard.is_pressed('p'):
        detectPose = not detectPose
        print("Switching Mode: Take finger Off Key")
        time.sleep(1)
    elif keyboard.is_pressed('h'):
        detectHand = not detectHand
        print("Switching Mode: Take finger Off Key")
        time.sleep(1)
    success, img = cap.read()
    if detectHand:
        img = detectorHand.findHands(img)
        lmList = detectorHand.findPosition(img)
        if len(lmList) != 0:
            if lmList[targetPoint]:
                print(lmList[targetPoint])
    if detectPose:
        img = detectorPose.findPose(img)
        lmList = detectorPose.findPosition(img)
        if len(lmList) != 0:
            if lmList[targetPoint]:
                print(lmList[targetPoint])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    img = cv2.flip(img, 1)
    cv2.putText(img, str(fps.__floor__()), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)