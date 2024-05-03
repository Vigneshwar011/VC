import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width 
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (122, 112, 222), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 50), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            return True
        else:
            return False

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=2)

buttonList = [['7', '8', '9', '*'],
              ['4', '5', '6', '-'],
              ['1', '2', '3', '+'],
              ['C', '0', '.', '=']]

buttons = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttons.append(Button((xpos, ypos), 100, 100, buttonList[y][x]))

myEquation = ''
delayCounter = 0

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 180), (255, 255, 255), cv2.FILLED)

    for button in buttons:
        button.draw(img)

    if hands:
        lmList = hands[0]['lmList']
        length, _, _ = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
        x, y = lmList[8][0:2]
        if length < 60:
            print(length, x, y)
            for i, button in enumerate(buttons):
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = buttonList[int(i % 4)][int(i / 4)]
                    print(myValue)

                    if myValue == "=":
                        try:
                            myEquation = str(eval(myEquation))
                        except:
                            myEquation = 'Error'
                    elif myValue == "C":  
                        myEquation = ''
                    else:
                        myEquation = myEquation + myValue
                    delayCounter = 1

    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    cv2.imshow("Virtual Calculator", img)
    key = cv2.waitKey(1)
    if key == 27:  
        break

cap.release()
cv2.destroyAllWindows()


