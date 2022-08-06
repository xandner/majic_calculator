import cv2
from cv2 import FONT_HERSHEY_PLAIN
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)
delay_counter=0

class Button:
    def __init__(self, position, width, height, value) -> None:
        self.pos = position
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (225, 225, 225), cv2.FILLED)

        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (20, 20, 20), 3)

        cv2.putText(
            img, self.value, (self.pos[0]+30, self.pos[1]+70), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)
    def check_click(self,x,y):
        if self.pos[0]<x<self.pos[0]+self.width \
            and self.pos[1]<y<self.pos[1]+self.height :
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (225, 225, 225), cv2.FILLED)

            cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                        (50,50,50), 3)

            cv2.putText(
            img, self.value, (self.pos[0]+20, self.pos[1]+70), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0), 5)

            return True
        else:
            return False

buttonListValues = [
                    ["7", "8", "9", "*"],
                    ["4", "5", "6","-"], 
                    ["1", "2", "3", "+"],
                    ["0", "/", ".", "="]
                ]

buttonList = []
for x in range(4):
    for y in range(4):
        x_pos = x*100+800
        y_pos = y*100+150
        buttonList.append(Button((x_pos, y_pos), 100, 100, buttonListValues[y][x]))


myEquation=''

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=False)
    cv2.rectangle(img,(800,70),(800+400,70+100),(255,255,255),cv2.FILLED)
    cv2.rectangle(img,(800,70),(800+400,70+100),(50,50,50),3)
    # cv2.rectangle(img,(800+70),(800+400,70+100),(50,50,50),3)
    for button in buttonList:
        button.draw(img)
    #chec hand
    if hands:
        lmList=hands[0]['lmList']        
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        x,y=lmList[8]
        if length<50:
            for i,button in enumerate(buttonList):
                print(delay_counter)
                if button.check_click(x,y) and delay_counter==0:
                    myValue=buttonListValues[int(i%4)][int(i/4)]
                    if myValue=="=":
                        myEquation=str(eval(myEquation))
                    else:
                        myEquation+=myValue
                    delay_counter=1

    if delay_counter!=0:
        delay_counter+=1
        if delay_counter>10:
            delay_counter=0

    cv2.putText(img,myEquation,(810,130),cv2.FONT_HERSHEY_PLAIN,3,(255,100,100),3)

    cv2.imshow("img", img)
    key = cv2.waitKey(1)
    if key==ord("c"):
        myEquation=""
