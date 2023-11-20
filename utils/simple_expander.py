import cv2
import numpy as np

from rembg import remove
from rembg.session_factory import new_session


class SimpleExpander:
    def remove_foreground(img, alpha_tolerance = 127, model = "u2net"):
        img_fg = remove(img, session=new_session(model))

        # 알파 채널을 이용하여 배경 이미지 추출
        alpha_channel = img_fg[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, alpha_tolerance, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        img_bg = cv2.bitwise_and(img, img, mask=mask_inv)

        return img_bg
    def determine_foreground_color(img, white_threshold = 250, black_threshold = 5):
        # 이미지를 알파 채널까지 포함하여 불러오기
        img_bg = SimpleExpander.remove_foreground(img)
        # 그레이스케일 변환
        gray = cv2.cvtColor(img_bg, cv2.COLOR_BGRA2GRAY)
        
        # 알파 채널이 있으면 투명 픽셀 제외
        if img_bg.shape[2] == 4:
            alpha_channel = img_bg[:, :, 3]
            visible_gray = gray[alpha_channel > 0]
        else:
            visible_gray = gray

        # 픽셀 값의 평균 계산
        mean_val = np.mean(visible_gray)

        # 흰색 또는 검정색에 가까운지 판단
        if mean_val > white_threshold:
            return "white", mean_val
        elif mean_val < black_threshold:
            return "black", mean_val
        else:
            return "nothing", mean_val

    def outpaint_simple_background(img, ratio = 2):
        pass