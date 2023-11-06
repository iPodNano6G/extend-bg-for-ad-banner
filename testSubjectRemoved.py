import cv2
from utils.border_remover import BorderRemover
from utils.foreground_remover import ForegroundRemover

mask_img = cv2.imread("mask.png", cv2.IMREAD_GRAYSCALE)
origin = cv2.imread("test.jpg", cv2.IMREAD_UNCHANGED)
origin = cv2.cvtColor(origin, cv2.COLOR_RGB2BGRA)
borderRemovedImg, _ = BorderRemover.remove_border(origin)
print(mask_img.shape)
print(borderRemovedImg.shape)

cv2.imwrite("result.png", ForegroundRemover.remove_subject(borderRemovedImg, mask_img))