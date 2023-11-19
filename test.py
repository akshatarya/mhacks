import cv2
from cvzone.PoseModule import PoseDetector
import ipdb
import cvzone
import time;
from pynput.keyboard import Key, Controller
from cvzone.HandTrackingModule import HandDetector

kb = Controller()



def get_col(x, width):
    if x <= width * 3.8: 
        return 1
    elif x < width * 4.9: 
        return 2
    else: 
        return 3


def get_row(y, height): 
    if y < height * 4: 
        return 1
    elif y < height * 4.75:
        return 2
    else: 
        return 3


# ipdb.set_trace()
detector = PoseDetector()
hand_detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error opening video")
curr_col = 2
curr_row = 2

success, img = cap.read()
(h, w) = img.shape[:2]
centerX, centerY = (w//2), (h//2)
colX = w//9
rowY = h//9

moved = True
count = 0
while(cap.isOpened()):
    success, img = cap.read()
    hands, img = hand_detector.findHands(img, draw=True, flipType=True)
    img = detector.findPose(img,draw=False)
    lmlist, bbox = detector.findPosition(img, draw=True, bboxWithHands=False)
    topLeft = img[0:centerY, 0:centerX]
    topRight = img[0:centerY, centerX:w]
    bottomLeft = img[centerY:h, 0:centerX]
    bottomRight = img[centerY:h, centerX:w]

    # print(bbox)

    if hands:
        # Information for the first hand detected
        hand1 = hands[0]  # Get the first hand detected
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        # Count the number of fingers up for the first hand
        fingers1 = hand_detector.fingersUp(hand1)
        print(f'H1 = {fingers1.count(1)}', end=" ")  # Print the count of fingers that are up

        # Calculate distance between specific landmarks on the first hand and draw it on the image
        length, info, img = hand_detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),
                                                  scale=10)

        # Check if a second hand is detected
        if len(hands) == 2:
            # Information for the second hand
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            center2 = hand2['center']
            handType2 = hand2["type"]

            # Count the number of fingers up for the second hand
            fingers2 = hand_detector.fingersUp(hand2)
            print(f'H2 = {fingers2.count(1)}', end=" ")

            # Calculate distance between the index fingers of both hands and draw it on the image
            length, info, img = hand_detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0),
                                                      scale=10)

        print(" ")  # New line for better readability of the printed output

    

    

    if bbox:
        if len(hands) == 2: 
        # prevDist=abs(center1[0] - center2[0])
        # print("++++++detected hands+++++++")
        # if(prevDist) <= bbox["bbox"][2] * 1.15:
        #     print("*******Correct Check*******")
            if(abs(center1[0] - center2[0])) >= bbox["bbox"][2] * 1.15:
            # if abs(center1[0] - center2[0]) > abs(center[0] * 1.15): 
                print("-------------------SPACE-------------------")
                kb.tap(Key.space)
                # count += 1
                # prevDist=abs(center1[0] - center2[0])
                # moved = False

        center = bbox["center"]

        next_col = get_col(center[0], colX)
        next_row = get_row(center[1], rowY)

        print(center)
        print("column", sep = " ")
        print(get_col(center[0], colX))
        print("row", sep=" ")
        print(get_row(center[1], rowY))
        if (next_col != curr_col): 
            diff_col = next_col - curr_col
            if (diff_col == -1): 
                print("Moved 1 left")
                kb.press(Key.right) 
                kb.release(Key.right)
                # moved == True
            else: 
                print("Moved 1 right")
                kb.press(Key.left) 
                kb.release(Key.left)
                # moved == True

            curr_col = next_col 

        if (next_row != curr_row):
            diff_row = next_row - curr_row
            if(curr_row == 1 and next_row == 2): 
                curr_row = next_row
                continue
            elif(curr_row == 3 and next_row == 2):
                curr_row = next_row
                continue
            elif (diff_row == -1): 
                print("Moved 1 up-------------------")
                kb.tap(Key.up)
                # moved == True
            else: 
                print("Moved 1 down---------------")
                kb.tap(Key.down)
                # moved == True

            curr_row = next_row

    # cv2.imshow("Image", img)
    cv2.waitKey(1)











# import cv2
# from cvzone.PoseModule import PoseDetector
# import ipdb
# import cvzone
# import time
# from pynput.keyboard import Key, Controller
# from cvzone.HandTrackingModule import HandDetector

# kb = Controller()



# def get_col(oldX, newX, bbox_width):
#     # print("X-val")
#     # print(newX - oldX)
#     # print("XWidth")
#     # print(bbox_width//3)
#     if(newX - oldX > bbox_width//2):
#         return 3
#     elif (oldX - newX > bbox_width//2): 
#         return 1
#     else: return 2

# def get_row(oldY, newY, bbox_height):
#     # print("Y-val")
#     # print("YWidth")
#     # print(newY - oldY)
#     # print(bbox_height//3)
#     if(newY - oldY > bbox_height//12):
#         return 3
#     elif (oldY - newY > bbox_height//7): 
#         return 1
#     else: return 2

# # def get_col(x, width):
# #     if x <= width * 3.8: 
# #         return 1
# #     elif x < width * 4.9: 
# #         return 2
# #     else: 
# #         return 3


# # def get_row(y, height): 
# #     if y < height * 4: 
# #         return 1
# #     elif y < height * 4.75:
# #         return 2
# #     else: 
# #         return 3


# # ipdb.set_trace()
# detector = PoseDetector()
# hand_detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Error opening video")
# curr_col = 2
# curr_row = 2

# success, img = cap.read()
# (h, w) = img.shape[:2]
# centerX, centerY = (w//2), (h//2)



# # count = 0
# # relative_center = [0,0]

# oldX=9999
# oldY=9999
# while(cap.isOpened()):

#     success, img = cap.read()
#     hands, img = hand_detector.findHands(img, draw=True, flipType=True)
#     img = detector.findPose(img,draw=False)
#     lmlist, bbox = detector.findPosition(img, draw=True, bboxWithHands=False)
#     topLeft = img[0:centerY, 0:centerX]
#     topRight = img[0:centerY, centerX:w]
#     bottomLeft = img[centerY:h, 0:centerX]
#     bottomRight = img[centerY:h, centerX:w]

#     # print(bbox)

#     if hands:
#         # Information for the first hand detected
#         hand1 = hands[0]  # Get the first hand detected
#         lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
#         bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
#         center1 = hand1['center']  # Center coordinates of the first hand
#         handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

#         # Count the number of fingers up for the first hand
#         fingers1 = hand_detector.fingersUp(hand1)
#         #print(f'H1 = {fingers1.count(1)}', end=" ")  # Print the count of fingers that are up

#         # Calculate distance between specific landmarks on the first hand and draw it on the image
#         length, info, img = hand_detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),
#                                                   scale=10)

#         # Check if a second hand is detected
#         if len(hands) == 2:
#             # Information for the second hand
#             hand2 = hands[1]
#             lmList2 = hand2["lmList"]
#             bbox2 = hand2["bbox"]
#             center2 = hand2['center']
#             handType2 = hand2["type"]

#             # Count the number of fingers up for the second hand
#             fingers2 = hand_detector.fingersUp(hand2)
#             #print(f'H2 = {fingers2.count(1)}', end=" ")

#             # Calculate distance between the index fingers of both hands and draw it on the image
#             length, info, img = hand_detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0),
#                                                       scale=10)

#         #print(" ")  # New line for better readability of the printed output

    

    

#     if bbox:
#         center = bbox["center"]
#         if(oldX==9999): oldX=center[0]
#         if(oldY==9999): oldY=center[1]
#         colX = bbox["bbox"][2]
#         rowY = bbox["bbox"][3]
#         if len(hands) == 2: 
#         # prevDist=abs(center1[0] - center2[0])
#         # print("++++++detected hands+++++++")
#         # if(prevDist) <= bbox["bbox"][2] * 1.15:
#         #     print("*******Correct Check*******")
#             if(abs(center1[0] - center2[0])) >= bbox["bbox"][2] * 1.15:
#             # if abs(center1[0] - center2[0]) > abs(center[0] * 1.15): 
#                 #print("-------------------SPACE-------------------")
#                 kb.tap(Key.space)
#                 # count += 1
#                 # prevDist=abs(center1[0] - center2[0])
#                 # moved = False

        


        
#         # if center[0] > center[0] * 0.9 and center[0] < center[0] * 1.1: 
#         #     count += 1
#         #     if count == 10: 
#         #         relative_center = [center[0], center[1]]
#         #         print(f"Relative Center: ({relative_center[0]}, {relative_center[1]})")
#         # else: 
#         #     count = 0
#         #     relative_center = [0,0]
        
        


#         next_col = get_col(oldX, center[0], colX)
#         next_row = get_row(oldY, center[1], rowY)

#         print(center)
#         print("column", sep = " ")
#         print(get_col(oldX, center[0], colX))
#         print("row", sep=" ")
#         print(get_row(oldY, center[1], rowY))
#         if (next_col != curr_col): 
#             diff_col = next_col - curr_col
#             if (diff_col == -1): 
#                 print("Moved 1 left")
#                 oldX=center[0]
#                 oldY=center[1]
#                 kb.press(Key.right) 
#                 kb.release(Key.right)
#                 # moved == True
#             else: 
#                 print("Moved 1 right")
#                 oldX=center[0]
#                 oldY=center[1]
#                 kb.press(Key.left) 
#                 kb.release(Key.left)
#                 # moved == True

#             curr_col = next_col 

#         if (next_row != curr_row):
#             diff_row = next_row - curr_row
#             if(curr_row == 1 and next_row == 2): 
#                 curr_row = next_row
#                 continue
#             elif(curr_row == 3 and next_row == 2):
#                 curr_row = next_row
#                 continue
#             elif (diff_row == -1): 
#                 print("Moved 1 up-------------------")
#                 oldX=center[0]
#                 oldY=center[1]
#                 kb.tap(Key.up)
#                 # moved == True
#             else: 
#                 print("Moved 1 down---------------")
#                 oldX=center[0]
#                 oldY=center[1]
#                 kb.tap(Key.down)
#                 # moved == True

#             curr_row = next_row
        

#     cv2.imshow("Image", img)
#     cv2.waitKey(1)
