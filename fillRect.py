import cv2, os,re, json, math
import numpy as np
from utils.border_remover import BorderRemover
from utils.mask_generator import MaskGenerator
from utils.simple_expander import SimpleExpander
import matplotlib.pyplot as plt
from dtaidistance import dtw# pip3 dtaidinstance

from sklearn.cluster import KMeans
from collections import Counter


def detect_is_simple(shadow_edges, complexity_edges, start_x=None, end_x=None, start_y=None, end_y=None ,threshold1=50,threshold2=12):
    return np.sum(shadow_edges[start_y:end_y,start_x:end_x] > 0) < threshold1 and np.sum(complexity_edges[start_y:end_y,start_x:end_x] > 0) < threshold2

def get_dominant_color(np_image):
    ## K-Means sklearn 라이브러리 chat-gpt 코드
    kmeans = KMeans(n_clusters=3, n_init='auto')
    kmeans.fit(np_image)
    
    # 각 클러스터의 레이블
    labels = kmeans.labels_
    
    # 레이블의 빈도 계산
    label_counts = Counter(labels)
    
    # 가장 큰 클러스터의 레이블 찾기
    largest_cluster_label = label_counts.most_common(1)[0][0]
    
    # 가장 큰 클러스터의 색상 추출
    dominant_color = kmeans.cluster_centers_[largest_cluster_label].astype(np.uint8)
    
    return dominant_color

def get_color_distance(labColor, dominantColor):
    return np.sqrt(np.sum(np.power(labColor - dominantColor, 2)))

def blend_colors(color1, color2, ratio):
    return tuple(int((1 - ratio) * c1 + ratio * c2) for c1, c2 in zip(color1, color2))

def fill_rectangular_region(image, rect_start, rect_end):#np slicing과 좌표처리가 같음. rect_end x좌표는 (해당 영역의 마지막 x좌표 + 1)
    # 좌우 경계 내외 2픽셀 이미지 기둥 정보 얻기
    left_pillar = np.copy(image[:, max(rect_start - 1, 0):rect_start+1])
    right_pillar = np.copy(image[:, (rect_end-1):min(rect_end+1, image.shape[1])])

    # 내부를 채우기
    left_pillar_color = []
    right_pillar_color = []

    for y in range(image.shape[0]):
        left_color = np.mean(left_pillar[y, :], axis=0)
        right_color = np.mean(right_pillar[y, :], axis=0)
        left_pillar_color.append(left_color)
        right_pillar_color.append(right_color)
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
    return left_pillar_color, right_pillar_color

# 이미지 로드
# image = cv2.imread('test.jpg')

# # 직사각형 좌표 (좌상단, 우하단)
# rect_start = (100, 0)
# rect_end = (image.shape[1]- 100, image.shape[0])

# # 내부를 채우기
# fill_rectangular_region(image, rect_start, rect_end)

# # 결과를 출력
# cv2.imwrite('result.jpg', image)

if 'SimpleNoblurred' not in os.listdir('./images'):
    os.mkdir('./images/SimpleNoblurred')
if 'SimpleBlurred' not in os.listdir('./images'):
    os.mkdir('./images/SimpleBlurred')

json_data = {}
loop_count = 0

test_mode = "division" # division, analysis

for filename in os.listdir('./images/'): 
    # Read image...
    if not re.match(r'^.+\.(jpg|jpeg|png)$', filename):
        continue
    # if loop_count >= 10:
    #     break
    # loop_count += 1
    print("Read", filename+"...")
    basename, extension = filename.split(".")[:2]
    
    origin = cv2.imread(os.path.join('./images/', filename))
    origin_4channel = cv2.cvtColor(origin, cv2.COLOR_RGB2RGBA)
    border_removed_image, _ = BorderRemover.remove_border(origin_4channel)
    #gray_scale_image = cv2.cvtColor(border_removed_image, cv2.COLOR_RGB2GRAY)

    # Load mask and get area
    mask = MaskGenerator.load_mask("masks/", basename)
    mask_start = None
    mask_end = None
    for x in range(mask.shape[1]):
        if np.any(mask[:,x] == 0):
            mask_start = x
            break
    for x in range(mask.shape[1]-1, -1, -1):
        if np.any(mask[:,x] == 0):
            mask_end = x
            break
    
    # rect_end는 확장 영역의 최우측보다 1픽셀 큰 인덱스의 좌표다.
    rect_start = max(0, mask_start-20)
    rect_end = min(mask_end+20, border_removed_image.shape[1])
    
    if test_mode == "analysis":# 색상 채우기 및 이미지 분석을 위한 그래프 생성
        # rect_start ~ rect_end 영역 채우기 및 참조 영역 색상 데이터 반환
        left_pillar_color, right_pillar_color = fill_rectangular_region(border_removed_image, rect_start, rect_end)
        ## 단색 판단
        # 색상 K-mean값 추출
        left_dominant_color = get_dominant_color(left_pillar_color)
        right_dominant_color = get_dominant_color(right_pillar_color)
        # 케니 기반 단색 판단
        isLeftSimple, isRightSimple = SimpleExpander.is_simple(border_removed_image)
        # 색상-거리 값 추출
        color_distances_left = [get_color_distance(c, left_dominant_color) for c in left_pillar_color]
        color_distances_right = [get_color_distance(c, right_dominant_color) for c in right_pillar_color]
        json_data[basename] = {
            "isSimple": bool(isLeftSimple and isRightSimple),#단색 판단 결과
            "dtwDistance": int(dtw.distance(color_distances_left, color_distances_right))# Dynamic Timing Warping
        }
        
        # 블러 추가 저장
        blurred_inner_image = cv2.GaussianBlur(border_removed_image, (13, 13), 11)
        blurred_image = border_removed_image.copy()
        blurred_image[:,rect_start:rect_end] = blurred_inner_image[:,rect_start:rect_end]
        
        #확장 참조 영역 색상 편차 분석
        plt.xlim(0,100)
        plt.gca().invert_yaxis()
        plt.plot(color_distances_left, range(len(color_distances_left)))
        plt.plot(color_distances_right, range(len(color_distances_right)))
        plt.savefig(os.path.join('./images/SimpleNoblurred', basename+"_graph.jpg"), format='jpeg')
        plt.clf()

        #확장 참조 영역 좌우 차이 분석
        plt.xlim(-50,50)
        plt.gca().invert_yaxis()
        plt.plot(np.copy(color_distances_left)-np.copy(color_distances_right), range(len(color_distances_right)))
        plt.savefig(os.path.join('./images/SimpleNoblurred', basename+"_diff.jpg"), format='jpeg')
        plt.clf()


        cv2.imwrite(os.path.join('./images/SimpleNoblurred', basename+"_result."+extension),border_removed_image)
        cv2.imwrite(os.path.join('./images/SimpleBlurred', basename+"_result."+extension), blurred_image)
    if test_mode == "division":
        min_interval = 20
        div_pos_left = []
        div_pos_right = []
        div_isSimple_left = []
        div_isSimple_right = []
        #edge detector
        gray_scale_image = cv2.cvtColor(border_removed_image, cv2.COLOR_BGR2GRAY)
        shadow_edges = cv2.Canny(gray_scale_image, threshold1=3500, threshold2=4500, apertureSize=7)
        complexity_edges = cv2.Canny(gray_scale_image, threshold1=30, threshold2=30)
        ## Check background complexity from left divided area of image
        current_x = 0
        first_interval = min(rect_start % min_interval + min_interval, rect_start) # longer than interval
        k = max(math.floor((rect_start - min_interval)/min_interval), 0) # number of splits(NOT number of divded piece)
        
        div_isSimple_left.append((detect_is_simple(shadow_edges, complexity_edges, current_x, current_x+first_interval)))
        div_pos_left.append(current_x)
        current_x = first_interval
        for _ in range(k):
            div_isSimple_left.append((detect_is_simple(shadow_edges, complexity_edges, current_x, current_x+min_interval)))
            div_pos_left.append(current_x)
            current_x += min_interval
        div_pos_left.append(rect_start)
        div_isSimple_left.append(False)
        
        ## Check background complexity from left divided area of image
        current_x = rect_end
        remain_length = border_removed_image.shape[1] - rect_end
        last_interval = min(remain_length % min_interval + min_interval, remain_length)
        k = max(math.floor((border_removed_image.shape[1] - rect_end - min_interval)/min_interval), 0)
        
        for _ in range(k):
            div_isSimple_right.append((detect_is_simple(shadow_edges, complexity_edges, current_x, current_x+min_interval)))
            div_pos_right.append(current_x)
            current_x += min_interval
        div_isSimple_right.append((detect_is_simple(shadow_edges, complexity_edges, current_x, current_x+last_interval)))
        div_pos_right.append(current_x)
        
        # 좌표 정보 및 단색 여부 정보 concat
        posList = np.concatenate((div_pos_left,div_pos_right),axis=0)
        isSimpleList = np.concatenate((div_isSimple_left,div_isSimple_right),axis=0)
        
        # 
        target_image = border_removed_image.copy()
        
        fill_start = None
        fill_flag = False
        fill_history = []
        print(posList)
        print(isSimpleList)
        for pos, isSimple in zip(posList.tolist(), isSimpleList.tolist()):
            if not fill_flag:
                if not isSimple:
                    fill_start = pos
                    fill_flag = True
            else:
                if isSimple:
                    fill_rectangular_region(target_image, fill_start, pos)
                    fill_history.append([fill_start, pos])
                    fill_flag = False
        if fill_flag:
            fill_rectangular_region(target_image, fill_start, target_image.shape[1])
            fill_history.append([fill_start, target_image.shape[1]])
        cv2.imwrite(os.path.join('./images/SimpleNoblurred', basename+"_div."+extension), target_image)
        isLeftSimple, isRightSimple = SimpleExpander.is_simple(border_removed_image)
        json_data[basename] = {
            "fillHistory": fill_history,
            "isSimple": bool(isLeftSimple and isRightSimple)
        }
        
        # add original version
        fill_rectangular_region(border_removed_image, rect_start, rect_end)
        cv2.imwrite(os.path.join('./images/SimpleNoblurred', basename+"_result."+extension), border_removed_image)
        
        
    
with open('./images/SimpleNoblurred/simpleInfo.json', "w") as f:
    json.dump(json_data, f, indent=4)

