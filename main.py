import math
import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# capture video from camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# setting Minimum Detection Confidence Threshold to 0.8
detector = HandDetector(detectionCon=0.8)

# volume control library pycaw usage
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

while cap.isOpened():
    success, img = cap.read()
    allHands, img = detector.findHands(img)
    if len(allHands) > 0:
        landMarkList = allHands[0]['lmList']
        thumbX, thumbY = landMarkList[4][0], landMarkList[4][1]
        indexX, indexY = landMarkList[8][0], landMarkList[8][1]
        cv2.circle(img, (thumbX, thumbY), 12, (255, 123, 100), cv2.FILLED)
        cv2.circle(img, (indexX, indexY), 12, (255, 123, 100), cv2.FILLED)
        length = math.dist((thumbX, thumbY), (indexX, indexY))
        vol = np.interp(length, [30, 200], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
    cv2.imshow("Hand Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()


