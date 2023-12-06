import cv2, os,re 
import numpy as np
from utils.border_remover import BorderRemover
from utils.mask_generator import MaskGenerator

def blend_colors(color1, color2, ratio):
    return tuple(int((1 - ratio) * c1 + ratio * c2) for c1, c2 in zip(color1, color2))

def fill_rectangular_region(image, rect_start, rect_end):
    # 좌우 바깥의 2픽셀 이미지 기둥 정보 얻기
    left_pillar = np.copy(image[:, max(rect_start - 1, 0):rect_start+1])
    right_pillar = np.copy(image[:, rect_end:min(rect_end+2, image.shape[1])])

    # 내부를 채우기
    for y in range(image.shape[0]):
        left_color = np.mean(left_pillar[y, :], axis=0)
        right_color = np.mean(right_pillar[y, :], axis=0)
        for x in range(rect_start, rect_end):
            # 각 픽셀의 좌우 기둥 색상 정보

            # 거리비례 색상 혼합
            distance_to_left = x - rect_start
            distance_to_right = rect_end - x
            total_distance = distance_to_left + distance_to_right

            right_ratio = distance_to_left / total_distance

            # 혼합된 색상으로 픽셀 값 설정
            blended_color = blend_colors(left_color, right_color, right_ratio)
            image[y, x] = blended_color

# 이미지 로드
# image = cv2.imread('test.jpg')

# # 직사각형 좌표 (좌상단, 우하단)
# rect_start = (100, 0)
# rect_end = (image.shape[1]- 100, image.shape[0])

# # 내부를 채우기
# fill_rectangular_region(image, rect_start, rect_end)

# # 결과를 출력
# cv2.imwrite('result.jpg', image)

if 'debug' not in os.listdir('./images'):
    os.mkdir('./images/debug')


for filename in os.listdir('./images/'): 
    if not re.match(r'^.+\.(jpg|jpeg|png)$', filename):
        continue

    print("Read", filename+"...")
    basename, extension = filename.split(".")[:2]
    if basename+"_result."+extension in os.listdir('./images/debug'):
        print(basename, "already exist")
        continue
    origin = cv2.imread(os.path.join('./images/', filename))
    origin = cv2.cvtColor(origin, cv2.COLOR_RGB2RGBA)

    borderRemovedImg, _ = BorderRemover.remove_border(origin)
    mask = MaskGenerator.load_mask("masks/", basename)
    rect_start = None
    rect_end = None
    for x in range(mask.shape[1]):
        if np.any(mask[:,x] == 0):
            rect_start = x
            break
    for x in range(mask.shape[1]-1, -1, -1):
        if np.any(mask[:,x] == 0):
            rect_end = x
            break
    
    print(borderRemovedImg.shape,max(0, rect_start-10), min(rect_end+10, borderRemovedImg.shape[1] - 1))
    fill_rectangular_region(borderRemovedImg, max(0, rect_start-10), min(rect_end+10, borderRemovedImg.shape[1] - 1))
    cv2.imwrite(os.path.join('./images/debug', basename+"_result."+extension),borderRemovedImg)

