import cv2 as cv
import sys


image =  cv.imread(cv.samples.findFile("TheCyborgs.png"))

if image is None:
    sys.exit("Could not read the image.")
cv.imshow("Image", image)
k = cv.waitKey(0)