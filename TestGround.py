import numpy as np
import cv2
from mss import mss
from PIL import Image
import HandTrackingModule as htm

bounding_box = {'top': 0, 'left': 0, 'width': 2000, 'height': 2000}

sct = mss()
detectorHand = htm.handDetector()
targetPoint = 0

while True:
    sct_img = sct.grab(bounding_box)
    sct_img = cv2.cvtColor(np.array(sct_img), cv2.COLOR_RGBA2RGB)
    cv2.imshow('screen', np.array(sct_img))
    img = detectorHand.findHands(np.array(sct_img))
    lmList = detectorHand.findPosition(img)
    if len(lmList) != 0:
        if lmList[targetPoint]:
            print(lmList[targetPoint])
    cv2.imshow('screen', img)
    cv2.waitKey(1)