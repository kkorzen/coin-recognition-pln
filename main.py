import cv2
import numpy as np
import cvzone

# ============================================
# === Camera <> coins distance = 16cm ========
# ============================================

one_grosz_size = 3310
ten_grosz_size = 4033
twenty_grosz_size = 5021
fifty_grosz_size  = 6000
one_zloty_size = 7900
two_zloty_size = 7100
five_zloty_size = 8550

hysteresis = 350

total_amount = 0
total_money = 0

cannyThreshWindows = "cannyThreshWindow"
coinAdjustWindow = "coinAdjustWindow"

#====== Flag for mode changing =========
differentiate_coins = 1
#=======================================

coin_denomination = 0.2

# ====================================
# === Debug only =====================
# ====================================

is_debug = 1

def AdjustCannyThresholdsWindow():
    cv2.namedWindow(cannyThreshWindows)
    cv2.resizeWindow(cannyThreshWindows, 640,240)
    cv2.createTrackbar('Threshold_1', cannyThreshWindows, 50, 255, lambda x:0)
    cv2.createTrackbar('Threshold_2', cannyThreshWindows, 100, 255, lambda x:0)

def AdjustCoinSizesWindow():
    cv2.namedWindow(coinAdjustWindow)
    cv2.resizeWindow(coinAdjustWindow, 400,400)
    cv2.createTrackbar('one_gr', coinAdjustWindow, 0, 10000, lambda x:0)
    cv2.createTrackbar('two_gr', coinAdjustWindow, 0, 10000, lambda x:0)
    cv2.createTrackbar('five_gr', coinAdjustWindow, 0, 10000, lambda x:0)
    cv2.createTrackbar('ten_gr', coinAdjustWindow, 0, 10000, lambda x:0)
    cv2.createTrackbar('twenty_gr', coinAdjustWindow, 0, 10000, lambda x:0)
    cv2.createTrackbar('fifty_gr', coinAdjustWindow, 0, 10000, lambda x:0)
    cv2.createTrackbar('one_zl', coinAdjustWindow, 0, 10000, lambda x:0)
    cv2.createTrackbar('two_zl', coinAdjustWindow, 0, 10000, lambda x:0)
    cv2.createTrackbar('five_zl', coinAdjustWindow, 0, 10000, lambda x:0)

def AdjustCoinSizes():
    global one_grosz_size
    global two_grosz_size
    global five_grosz_size
    global ten_grosz_size
    global twenty_grosz_size
    global fifty_grosz_size
    global one_zloty_size
    global two_zloty_size
    global five_zloty_size

    one_grosz_size = cv2.getTrackbarPos("one_gr", coinAdjustWindow)
    two_grosz_size = cv2.getTrackbarPos("two_gr", coinAdjustWindow)
    five_grosz_size = cv2.getTrackbarPos("five_gr", coinAdjustWindow)
    ten_grosz_size = cv2.getTrackbarPos("ten_gr", coinAdjustWindow)
    twenty_grosz_size = cv2.getTrackbarPos("twenty_gr", coinAdjustWindow)
    fifty_grosz_size  = cv2.getTrackbarPos("fifty_gr", coinAdjustWindow)
    one_zloty_size = cv2.getTrackbarPos("one_zl", coinAdjustWindow)
    two_zloty_size = cv2.getTrackbarPos("two_zl", coinAdjustWindow)
    five_zloty_size = cv2.getTrackbarPos("five_zl", coinAdjustWindow)

if is_debug:
    AdjustCannyThresholdsWindow()
    AdjustCoinSizesWindow()
    

# ====================================
# ====================================
# ====================================

def PreProcessing(_img):
    prep_img = cv2.GaussianBlur(_img, (123,123), 3)
    if is_debug:
        thresh_1 = cv2.getTrackbarPos("Threshold_1", cannyThreshWindows)
        thresh_2 = cv2.getTrackbarPos("Threshold_2", cannyThreshWindows)
        AdjustCoinSizes()
    else:
        thresh_1 = 50
        thresh_2 = 100
    prep_img = cv2.Canny(prep_img, thresh_1, thresh_2)
    kernel = np.ones((3,3), np.uint8)
    prep_img = cv2.dilate(prep_img, kernel, iterations=1)
    cv2.morphologyEx(prep_img, cv2.MORPH_CLOSE, kernel)
    return prep_img

def IdentifyCoin(_coin_size):
    if one_grosz_size - hysteresis < area < one_grosz_size + hysteresis:
        return 0.01
    if ten_grosz_size - hysteresis < area < ten_grosz_size + hysteresis:
        return 0.10
    if twenty_grosz_size - hysteresis < area < twenty_grosz_size + hysteresis:
        return 0.20
    if fifty_grosz_size - hysteresis < area < fifty_grosz_size + hysteresis:
        return 0.50
    if one_zloty_size - hysteresis < area < one_zloty_size + hysteresis:
        return 1
    if two_zloty_size - hysteresis < area < two_zloty_size + hysteresis:
        return 2
    if five_zloty_size - hysteresis < area < five_zloty_size + hysteresis:
        return 5
    return 0

vid = cv2.VideoCapture(1)

if not vid.isOpened():
    print("Could not open video capture device. Exiting...")
    exit(1)

while True:

    total_amount = 0
    total_money = 0

    is_success, frame = vid.read()

    prep_frame = PreProcessing(frame)

    img_countours, contours_found = cvzone.findContours(frame, prep_frame, minArea=20)

    if contours_found is not None:
        for contour in contours_found:
            peri = cv2.arcLength(contour["cnt"], True)
            approx = cv2.approxPolyDP(contour["cnt"], 0.02 * peri, True)

            # len(approx) for circles is almost always eqaul to 8
            # so to check the shape, the condition below has to be used
            # value of 6 is used just to make the detection range wider

            if len(approx) >= 6:
                area = contour["area"]
                total_amount += 1

                if(differentiate_coins):
                    total_money += IdentifyCoin(area)
                    # printing the value of area was not removed to make adjusting a coin size easier
                    print(area)
                    

                

    stacked_img = cvzone.stackImages([frame, prep_frame], 2, 1)
    if (not differentiate_coins):
        total_money = total_amount * coin_denomination
        
    cvzone.putTextRect(stacked_img, f'Coins counted: {total_amount} || PLN: {(total_money):.2f}', (320, 50), colorR=(0,0,255))
    cv2.imshow("Video capture", stacked_img)
   

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()