import cv2
import numpy as np

buzz = cv2.imread('buzz.png')
space = cv2.imread('space.jpg')
gray_buzz = cv2.cvtColor(buzz, cv2.COLOR_BGR2GRAY)
# new = np.zeros(np.shape(space), np.uint8)
_, mask = cv2.threshold(gray_buzz, 254, 255, cv2.THRESH_BINARY)
mask_inverse = cv2.bitwise_not(mask)
space_masked = cv2.bitwise_and(space, space, mask=mask)
buzz_masked = cv2.bitwise_and(buzz, buzz, mask=mask_inverse)
new = cv2.add(space_masked, buzz_masked)
# cv2.imshow('new', new)
cv2.imwrite('mask.jpg', mask)
cv2.imwrite('mask_inverse.jpg', mask_inverse)
cv2.imwrite('buzz_masked.jpg', buzz_masked)
cv2.imwrite('space_masked.jpg', space_masked)
cv2.imwrite('new.jpg', new)
cv2.waitKey(0)
cv2.destroyAllWindows()