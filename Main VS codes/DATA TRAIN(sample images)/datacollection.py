import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize the hand detector
detector = HandDetector(maxHands=1)

# Parameters
offset = 20
imgSize = 300
folder = r"C:\Users\DEATHSEC\Desktop\TCC2\TRAIN\Up"  # Use raw string for Windows path
capture_images = False
max_images = 5000  # Total number of images to capture when 's' is pressed
counter = 0

while True:
    success, img = cap.read()
    if not success:
        print("Error: Unable to capture image.")
        break

    if capture_images:
        if counter < max_images:
            hands, img = detector.findHands(img)
            
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                print(f"Bounding Box: x={x}, y={y}, w={w}, h={h}")

                # Calculate cropping coordinates ensuring they are within the image boundaries
                x_start = max(x - offset, 0)
                y_start = max(y - offset, 0)
                x_end = min(x + w + offset, img.shape[1])
                y_end = min(y + h + offset, img.shape[0])

                imgCrop = img[y_start:y_end, x_start:x_end]

                if imgCrop.size == 0:
                    print("Error: Cropped image is empty.")
                    continue

                # Create a white image to place the resized crop
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                aspectRatio = h / w

                # Resize image to fit within the square imgSize
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                # Save the image
                cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
                counter += 1
                print(f"Saved image {counter}")

            # Check if the desired number of images has been captured
            if counter >= max_images:
                print("Captured 1000 images. Stopping...")
                capture_images = False
                counter = 0  # Reset counter for the next session

    # Display the images
    cv2.imshow("Image", img)

    # Check for user input
    key = cv2.waitKey(1)
    if key == ord('s'):
        if not capture_images:
            print("Starting image capture...")
            capture_images = True
        else:
            print("Already capturing images.")
    elif key == ord('q'):
        print("Exiting...")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()