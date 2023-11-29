import cv2
import numpy as np

from rembg import remove
from rembg.session_factory import new_session


class SimpleExpander:
    @classmethod
    def remove_foreground(cls, img, alpha_tolerance = 127, model = "u2net"):#deprecated
        img_fg = remove(img, session=new_session(model))

        # 알파 채널을 이용하여 배경 이미지 추출
        alpha_channel = img_fg[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, alpha_tolerance, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        img_bg = cv2.bitwise_and(img, img, mask=mask_inv)

        return img_bg
    @classmethod
    def determine_foreground_color(cls, img, white_threshold = 250, black_threshold = 5):#deprecated
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

    @classmethod
    def is_simple(cls, img, ratio = 2):
        def analyze_complexity(src, threshold):
            gray_image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_image, threshold, threshold)
            edge_count = np.sum(edges > 0)
            return edge_count
        
        detect_length = 20
        edge_threshold = 12

        h,w = img.shape[:2]
        copy1, copy2 = None, None
        if(w/h < ratio):
            copy1 = img[:, :detect_length]
            copy2 = img[:, -detect_length:]
        else:
            copy1 = img[:detect_length]
            copy2 = img[-detect_length:]
        #분석 수행
        #entropy = analyze_color_diversity(extract_removed_image)
   
        edge_count_left = analyze_complexity(copy1, 50)
        edge_count_right = analyze_complexity(copy2, 50)
        print(edge_count_left, edge_count_right)
        return (edge_count_left < edge_threshold), (edge_count_right < edge_threshold)
    @classmethod
    def expand_simple(cls, img, ratio = 2, expand_direction = "both"):
        kernel = 41
        height, width = img.shape[:2]
        pad_left, pad_right, pad_top, pad_bottom = (0, 0, 0, 0)
        new_width, new_height = 0,0
        if(width/height < ratio):
            new_width = int(height * ratio) - width
        else:
            new_height = int(width // ratio) - height
        if(expand_direction == "both"):
            pad_left = int(new_width/2)
            pad_right = new_width - pad_left
            pad_top = int(new_height/2)
            pad_bottom = new_height - pad_top
        elif(expand_direction == "left"):
            pad_left = new_width
            pad_top = new_height
        elif(expand_direction == "right"):
            pad_right = new_width
            pad_bottom = new_height

        padded_image = cv2.copyMakeBorder(img, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_REPLICATE)

        #블러작업
        mask = np.zeros(padded_image.shape[:2], dtype=np.uint8)

        if pad_top > 0 and pad_left > 0:
            mask[:pad_top if pad_top > 0 else None, :pad_left if pad_left > 0 else None] = 1
        if pad_bottom > 0 and pad_right > 0:
            mask[-pad_bottom if pad_bottom > 0 else None:, -pad_right if pad_right > 0 else None:] = 1

        blurred_image = cv2.GaussianBlur(padded_image, (kernel, kernel), 150)
        
        padded_image = np.where(mask[:, :, np.newaxis] == 1, blurred_image, padded_image)
        
        return padded_image
