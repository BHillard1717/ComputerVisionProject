import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection()

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('LargerTestMp.mp4')

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    if results.detections:
        #mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.detections):
            print(lm.location_data.relative_bounding_box.xmin)
            bboxC = lm.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.xmin * iw), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            #cv2.rectangle(img, bbox, (255,0,255), 2)


            mpDraw.draw_detection(img, lm)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #img = cv2.flip(img, 1)
    #cv2.putText(img, str(fps.__floor__()), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
