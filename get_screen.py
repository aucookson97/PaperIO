import cv2
import numpy as np
from mss import mss
from PIL import Image
import pyautogui
import math
import time

purchasing_items_single = ((680, 585), (680, 507), (680, 462), (680, 423), (680, 372))
purchasing_items_multiple = ((420, 552), (420, 503), (420, 452), (420, 405), (420, 367))

top_crop = 250
lower_white = np.array([0, 0, 50])
upper_white = np.array([179, 20, 255])

sct = mss()
mon = {'top': 260, 'left': 350, 'width': 575, 'height': 400}

current_round = 1

def run():
    
    print 'Enter 1 When Ready: '
    while (input() != 1):
        pass
    print 'Starting!'
    
    blobDetector = createBlobDetector()

    playing = True


    # Start From Menu
    pyautogui.moveTo(660, 532, 1)
    pyautogui.click()
    time.sleep(3)


    while playing:

        img = np.array(sct.grab(mon))
        img = img[top_crop:400, :int(img.shape[1] / 1.75)]

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        brightness = np.mean(hsv)
        # Check for Round Complete:
        if (brightness < 50 and brightness > 10):
            nextRound()

        
        mask = cv2.inRange(hsv, lower_white, upper_white)
        reverse_mask = 255 - mask
        result = cv2.bitwise_and(img, img, mask=mask)

        keypoints = blobDetector.detect(reverse_mask)
        #img_with_kp = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Find farthest right guy
        if len(keypoints) > 0:
            priority = keypoints[0]
            for kp in keypoints:
                if kp.pt[0] > priority.pt[0]:
                    priority = kp

            target = (priority.pt[0] + 10, priority.pt[1])
            moveMouseToGamePoint(target)
            execute()

def nextRound():
    global current_round
    print 'Round {} Complete! Let\'s Buy Some Toys'.format(current_round)
    current_round += 1

    # Go To Purchasing
    time.sleep(3)
    pyautogui.moveTo(730, 632, .5)
    pyautogui.click()
    time.sleep(.5)

    for pt in purchasing_items_single:
        pyautogui.moveTo(pt[0], pt[1], .05)
        pyautogui.click()
        time.sleep(.05)
    for pt in purchasing_items_multiple:
        pyautogui.moveTo(pt[0], pt[1], .05)
        for i in range(10):
            pyautogui.click()
            time.sleep(.01)
        time.sleep(.05)

    # Start Next Round
    pyautogui.moveTo(860, 652, .25)
    pyautogui.click()

    


def execute():
    current_position = pyautogui.position()
    x, y = (current_position[0], mon['top'] + 20)
    pyautogui.dragTo(x, y, .25)

def distance(pt1, pt2):
    return math.sqrt(math.pow(pt1[0] - pt2[0], 2) + math.pow(pt1[1] - pt2[1], 2))

def screenToGame(screen_pt):
    x = mon['left'] + screen_pt[0]
    y = mon['top'] + screen_pt[1]

def imageToGame(image_pt):
    x = mon['left'] + image_pt[0]
    y = mon['top'] + top_crop + image_pt[1]
    return (x, y)

def moveMouseToGamePoint(image_pt):
    x, y = imageToGame(image_pt)
    pyautogui.moveTo(x, y, .01)

def createBlobDetector():
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 0
    params.maxThreshold = 256
    params.filterByArea = True
    params.filterByConvexity = False
    params.filterByCircularity = False
    params.filterByInertia = False
    params.minArea = 10
    params.maxArea = 1000
    detector = cv2.SimpleBlobDetector_create(params)
    return detector


if __name__ == "__main__":
    run()
