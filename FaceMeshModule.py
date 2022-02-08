import cv2
import mediapipe as mp
import time


class meshMaker():
    def __init__(self,
               static_image_mode=False,
               max_num_faces=1,
               refine_landmarks=False,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5 ):
        self.mode = static_image_mode
        self.max_num_faces = max_num_faces
        self.refineLandmarks = refine_landmarks
        self.detectCon = min_detection_confidence
        self.trackCon = min_tracking_confidence

        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.mode, self.max_num_faces, self.refineLandmarks, self.detectCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def makeMesh(self, img, draw=True):
        drawSpecs = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)

        if self.results.multi_face_landmarks:

            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_LIPS, drawSpecs, drawSpecs)
        return img

    def findPosition(self, img, pointNum=0, draw=True):
        lmList = []
        if self.results.multi_face_landmarks:
            myMesh = self.results.multi_face_landmarks[pointNum]

            for id, lm in enumerate(myMesh.landmark):
                # print(id,lm)

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), pointNum, (255, 0, 255), cv2.FILLED)

        return lmList

def main():
    cap = cv2.VideoCapture(0)
    detector = meshMaker()
    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()
        img = detector.makeMesh(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[12])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        img = cv2.flip(img, 1)
        cv2.putText(img, str(fps.__floor__()), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()