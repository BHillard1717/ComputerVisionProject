import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
FaceMesh = mpFaceMesh.FaceMesh(max_num_faces=3)
drawSpecs = mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(0,255,0))


pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = FaceMesh.process(imgRGB)

    if results.multi_face_landmarks:

        for faceLms in results.multi_face_landmarks:
            for id, lm in enumerate(faceLms.landmark):
                #print(id,lm)

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                #if id == 4:
                    #cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)

            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_LIPS, drawSpecs, drawSpecs)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    img = cv2.flip(img, 1)
    cv2.putText(img, str(fps.__floor__()), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
