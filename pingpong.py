{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "46ace388",
   "metadata": {},
   "outputs": [
    {
     "ename": "AttributeError",
     "evalue": "'NoneType' object has no attribute 'copy'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mAttributeError\u001b[0m                            Traceback (most recent call last)",
      "Input \u001b[1;32mIn [1]\u001b[0m, in \u001b[0;36m<cell line: 23>\u001b[1;34m()\u001b[0m\n\u001b[0;32m     23\u001b[0m _,img\u001b[38;5;241m=\u001b[39mcap\u001b[38;5;241m.\u001b[39mread()    \n\u001b[0;32m     24\u001b[0m img\u001b[38;5;241m=\u001b[39mcv2\u001b[38;5;241m.\u001b[39mflip(img,\u001b[38;5;241m1\u001b[39m)\n\u001b[1;32m---> 25\u001b[0m imgRaw\u001b[38;5;241m=\u001b[39m\u001b[43mimg\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mcopy\u001b[49m()\n\u001b[0;32m     26\u001b[0m hands,img\u001b[38;5;241m=\u001b[39mdetector\u001b[38;5;241m.\u001b[39mfindHands(img,flipType\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mFalse\u001b[39;00m)\n\u001b[0;32m     28\u001b[0m img \u001b[38;5;241m=\u001b[39m cv2\u001b[38;5;241m.\u001b[39maddWeighted(img,\u001b[38;5;241m0.2\u001b[39m,imgBackground,\u001b[38;5;241m0.8\u001b[39m,\u001b[38;5;241m0\u001b[39m)\n",
      "\u001b[1;31mAttributeError\u001b[0m: 'NoneType' object has no attribute 'copy'"
     ]
    }
   ],
   "source": [
    "import cv2\n",
    "import cvzone\n",
    "import numpy as np\n",
    "from cvzone.HandTrackingModule import HandDetector\n",
    "\n",
    "cap = cv2.VideoCapture(0)\n",
    "cap.set(3,1280)\n",
    "cap.set(4,720)\n",
    "imgBackground=cv2.imread('Background.png')\n",
    "imgGameOver=cv2.imread('gameOver.png')\n",
    "imgBall=cv2.imread('Ball.png',cv2.IMREAD_UNCHANGED)\n",
    "imgBat1=cv2.imread('bat1.png',cv2.IMREAD_UNCHANGED)\n",
    "imgBat2=cv2.imread('bat2.png',cv2.IMREAD_UNCHANGED)\n",
    "#hand detector\n",
    "detector=HandDetector(detectionCon=0.8,maxHands=2)\n",
    "\n",
    "ballpos=[100,100]\n",
    "speedx=20\n",
    "speedy=20\n",
    "score=[0,0]\n",
    "gameover=False\n",
    "while True:\n",
    "    _,img=cap.read()    \n",
    "    img=cv2.flip(img,1)\n",
    "    imgRaw=img.copy()\n",
    "    hands,img=detector.findHands(img,flipType=False)\n",
    "    \n",
    "    img = cv2.addWeighted(img,0.2,imgBackground,0.8,0)\n",
    "    #bring the bat\n",
    "    #check for hands\n",
    "    if hands:\n",
    "        for hand in hands:\n",
    "            x,y,w,h=hand['bbox']\n",
    "            #shape gives height width and channels\n",
    "            h1,w1,_=imgBat1.shape\n",
    "            y1=y-h1//2\n",
    "            y1=np.clip(y1,20,415)\n",
    "            if hand['type']==\"Left\":\n",
    "                img = cvzone.overlayPNG(img,imgBat1,(60,y1))\n",
    "                if 59<ballpos[0]<59+w1 and y1<ballpos[1]<y1+h1:\n",
    "                    speedx=-speedx\n",
    "                    ballpos[0]+=30\n",
    "                    score[0]+=5\n",
    "            if hand['type']==\"Right\":\n",
    "                img = cvzone.overlayPNG(img,imgBat2,(1195,y1))\n",
    "                if 1145<ballpos[0]<1165 and y1<ballpos[1]<y1+h1:\n",
    "                    speedx=-speedx\n",
    "                    ballpos[0]-=30\n",
    "                    score[1]+=5\n",
    "    #gameover\n",
    "    if ballpos[0]<40 or ballpos[0]>1200:\n",
    "        gameover=True\n",
    "    if gameover:\n",
    "        img=imgGameOver\n",
    "        cv2.putText(img,str(score[0]+score[1]).zfill(2),(585,360),cv2.FONT_HERSHEY_COMPLEX,2.5,(200,0,200),5)\n",
    "    #move the ball only if the game is not over\n",
    "    else:\n",
    "        #500 purple starting \n",
    "        if ballpos[1]>=500 or ballpos[1]<=10:\n",
    "            speedy=-speedy\n",
    "        \n",
    "        #moving ball\n",
    "        ballpos[0]+=speedx\n",
    "        ballpos[1]+=speedy\n",
    "        #draw the ball\n",
    "        img = cvzone.overlayPNG(img,imgBall,(ballpos))\n",
    "        cv2.putText(img,str(score[0]),(300,650),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),5)\n",
    "        cv2.putText(img,str(score[1]),(900,650),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,255),5)\n",
    "    #img[height:width]\n",
    "    img[580:700,20:233]=cv2.resize(imgRaw,(213,120))\n",
    "    cv2.imshow(\"Image\",img)\n",
    "    key=cv2.waitKey(1)\n",
    "    if key==ord('r'):\n",
    "        ballpos=[100,100]\n",
    "        speedx=20\n",
    "        speedy=20\n",
    "        score=[0,0]\n",
    "        gameover=False\n",
    "        imgGameOver=cv2.imread('gameOver.png')\n"
   ]
  },
  {
   "cell_type": "raw",
   "id": "2efd5fd0",
   "metadata": {},
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "41872d35",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e30cad7b",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
