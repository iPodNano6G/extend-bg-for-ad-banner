from utils.inpainter import Inpainter
import cv2

def find_object_bbox(image):
    # 투명 픽셀을 검출하기 위해 알파 채널을 추출
    alpha_channel = image[:, :, 3]

    # 알파 채널을 기반으로 피사체가 있는 영역의 좌표를 찾음
    non_zero_pixels = cv2.findNonZero(alpha_channel)
    left, top, width, height = cv2.boundingRect(non_zero_pixels)

    # 최소 크기의 직사각형의 좌표를 반환
    return left, top, left + width, top + height

image_path = r"C:\projects\extend-bg-for-ad-banner\extract\border_removed_result\AT75XX00012.jpg"
save_path = "result2.png"
mask_path= r"C:\projects\extend-bg-for-ad-banner\extract\border_removed_result\ps_background_removal2\AT75XX00012.png"

mask_img = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)

left, top, right, bottom = find_object_bbox(mask_img)
Inpainter().generative_extend_using_ps(image_path, save_path)