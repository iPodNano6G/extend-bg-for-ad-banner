import cv2
from rembg import remove
from rembg.session_factory import new_session

#배경을 제거하여 투명 픽셀로 대체
class ForegroundRemover:
    def remove_foreground(img, alpha_tolerance = 127, model = "u2net"):
        img_fg = remove(img, session=new_session(model))

        # 알파 채널을 이용하여 배경 이미지 추출
        alpha_channel = img_fg[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, alpha_tolerance, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        img_bg = cv2.bitwise_and(img, img, mask=mask_inv)

        return img_bg
