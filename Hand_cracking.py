# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:09:19 2022

@author: Toqa Alaa
"""
import cv2
import mediapipe as mp
import time


class Hand_detector():
    def __init__(self, mode= False, maxHands= 2, complexity=1, detectioncon= 0.5,trackconf= 0.5 ):
        self.mode= mode
        self.maxHands= maxHands
        self.comp= complexity
        self.detectioncon= detectioncon
        self.trackconf= trackconf
        
        self.mpHands= mp.solutions.hands
        self.hands= self.mpHands.Hands(self.mode, self.maxHands,
                                       self.comp,
                                       self.detectioncon,
                                       self.trackconf)
        self.mpDraw= mp.solutions.drawing_utils
        
        
    def findHands(self, img, draw=True):
        
        img_rgb= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results =self.hands.process(img_rgb)
    
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw: 
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS) 
        return img
      
    
    def find_pos(self, img, Hand_NO= 0, draw=True ):
        landmark_ls= []
        if self.results.multi_hand_landmarks:
            my_hand =self.results.multi_hand_landmarks[Hand_NO]
            
   
            for id, landmark in enumerate(my_hand.landmark):
                #print(id, landmark)
                h,w,c= img.shape
                cx, cy= int(landmark.x*w), int(landmark.y*h)
                #print(id, cx,cy)
                landmark_ls.append([id,cx,cy])
                #if (id==4):
                if draw:
                    cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
        
        return landmark_ls

    
def main():
    s_time= 0
    c_time= 0
    cap= cv2.VideoCapture(0)
    detector= Hand_detector()
    
    while True:
        success, img= cap.read()
        img =detector.findHands(img)
        landmark_ls= detector.find_pos(img)
        if len(landmark_ls) !=0:
            print(landmark_ls[4])
        c_time= time.time()
        fps= 1/(c_time- s_time)
        s_time= c_time
        
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3
                    ,(255,0,255), 3)
        
        
        cv2.imshow("image", img)
        cv2.waitKey(1)
        
 
    
if __name__== "__main__":
    main()
    
    
    
