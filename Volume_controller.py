# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 17:51:48 2022

@author: Toqa Alaa
"""

import cv2
import numpy as np
import time
import Hand_cracking as HTM
import math
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



cam_width, cam_height = 640, 480;
cap= cv2.VideoCapture(0)
cap.set(2, cam_width)
cap.set(4, cam_height)
s_time= 0
detector= HTM.Hand_detector(detectioncon=0.8)
vol= 0
vol_bar=400
vol_per= 0




devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volume_range= volume.GetVolumeRange()

min_volume= volume_range[0]
max_volume= volume_range[1]


while(True):
    
    success, img= cap.read()
    img= detector.findHands(img)
    landmark_list= detector.find_pos(img, draw= False)
    if len(landmark_list)!=0:
        #print(landmark_list[4], landmark_list[8])
        x1,y1= landmark_list[4][1], landmark_list[4][2]
        x2,y2= landmark_list[8][1], landmark_list[8][2]
        cx, cy= (x1+x2)//2, (y1+y2)//2
        
    
        
        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
    
        length= math.hypot(x2-x1, y2-y1)
        #print(length)
        
        if(length<20):
            cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)
        
        #length_range 50-300
        #volume range -65-0
        vol= np.interp(length, [50,300], [min_volume, max_volume])
        vol_bar= np.interp(length, [50,300],[400,150])
        vol_per= np.interp(length, [50,300], [0,100])
        volume.SetMasterVolumeLevel(vol, None)
        #print(volume)
        
    cv2.rectangle(img, (50,150), (85, 400), (255,0,0),3)
    cv2.rectangle(img, (50,int(vol_bar)), (85, 400), (255,0,0), cv2.FILLED)
    cv2.putText(img, f'{int(vol_per)} %', (40,450), cv2.FONT_HERSHEY_PLAIN,3
                ,(255,0,0), 3)
    
    c_time= time.time()
    fps= 1/(c_time- s_time)
    s_time= c_time
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3
                ,(255,0,255), 3)
    
    cv2.imshow("image", img)
    cv2.waitKey(1)