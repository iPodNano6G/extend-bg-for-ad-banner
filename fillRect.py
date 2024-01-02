import cv2, os,re, json, math
import numpy as np
from utils.border_remover import BorderRemover
from utils.mask_generator import MaskGenerator
from utils.simple_expander import SimpleExpander
import matplotlib.pyplot as plt #pip3 install matplotlib
from dtaidistance import dtw #pip3 install dtaidinstance

from sklearn.cluster import KMeans #pip3 install scikit-learn
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

def generate_gradient_image(image, left=None, right=None, top=None, bottom=None, expand_type=(True,True)):
    #expand_type = (좌우 참조, 상하 참조)
    left = 0 if left is None else left
    right = image.shape[1] if right is None else right
    top = 0 if top is None else top
    bottom = image.shape[0] if bottom is None else bottom
    
    width = right - left
    height = bottom - top

    if expand_type[0] == True:
        left_color = np.copy(np.mean(image[top:bottom, max(left-1, 0):left+1], axis=1))
        right_color = np.copy(np.mean(image[top:bottom, (right-1):min(right+1, image.shape[1])], axis=1))
    if expand_type[1] == True:
        top_color = np.copy(np.mean(image[max(top-1, 0):top+1, left:right], axis=0))
        bottom_color = np.copy(np.mean(image[(bottom-1):min(bottom+1, image.shape[0]), left:right], axis=0))
        
    # Create coordinate grids
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Calculate color values using vectorized operations
    result = np.zeros((height, width, 3))
    if all(expand_type):
        for c in range(3):
            result[:,:,c] = (
                0.5 * ((width - 1 - x) * left_color[y, c] + x * right_color[y, c]) / (width - 1) +
                0.5 * ((height - 1 - y) * top_color[x, c] + y * bottom_color[x, c]) / (height - 1)
            )
    elif expand_type[0] == True:
        for c in range(3):
            result[:,:,c] = (
                ((width - 1 - x) * left_color[y, c] + x * right_color[y, c]) / (width - 1)
            )
    elif expand_type[1] == True:
        for c in range(3):
            result[:,:,c] = (
                ((height - 1 - y) * top_color[x, c] + y * bottom_color[x, c]) / (height - 1)
            )
    result = cv2.cvtColor(result.astype(np.uint8),cv2.COLOR_RGB2RGBA)
    
    return result

# 이미지 로드
# image = cv2.imread('test.jpg')

# # 직사각형 좌표 (좌상단, 우하단)
# rect_start = (100, 0)
# rect_end = (image.shape[1]- 100, image.shape[0])

# # 내부를 채우기
# fill_rectangular_region(image, rect_start, rect_end)

# # 결과를 출력
# cv2.imwrite('result.jpg', image)


if __name__ == "__main__":
    #test
    # image = cv2.imread("test.jpg")
    # left, right, top, bottom = (300,450,300,450)
    # rs = generate_gradient_image(image, left, right, expand_type=(True, False))
    # cv2.imwrite('result.jpg', rs)
    # exit(0)
    
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
        rect_start = max(0, mask_start - 20)
        rect_end = min(mask_end + 20, border_removed_image.shape[1])
        
        if test_mode == "analysis":# 색상 채우기 및 이미지 분석을 위한 그래프 생성
            # rect_start ~ rect_end 영역 채우기 및 참조 영역 색상 데이터 반환
            result_img = generate_gradient_image(border_removed_image, rect_start, rect_end, expand_type=(True,False))
            left_pillar_color, right_pillar_color = result_img[:,0], result_img[:,result_img.shape[1]-1]#240101 테스트 미실시
            ## 단색 판단
            # 색상 K-mean값 추출 (좋지 않으므로 평균값으로 대체 예정)
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
        if test_mode == "division":# input: border_removed_image, rect_start, rect_end
            min_interval = 20
            posList = []
            isSimpleList = []
            
            #edge detector(important)
            gray_scale_image = cv2.cvtColor(border_removed_image, cv2.COLOR_BGR2GRAY)
            shadow_edges = cv2.Canny(gray_scale_image, threshold1=3500, threshold2=4500, apertureSize=7)
            complexity_edges = cv2.Canny(gray_scale_image, threshold1=30, threshold2=30)
            
            ## left area - Check background complexity
            current_x = 0
            first_interval = min(rect_start % min_interval + min_interval, rect_start) # longer than interval
            k = max(math.floor((rect_start - min_interval)/min_interval), 0) # number of splits(warn. this is NOT number of divded piece)
            
            isSimpleList.append((detect_is_simple(shadow_edges, complexity_edges, current_x, current_x+first_interval)))
            posList.append(current_x)
            current_x = first_interval
            for _ in range(k):
                isSimpleList.append((detect_is_simple(shadow_edges, complexity_edges, current_x, current_x+min_interval)))
                posList.append(current_x)
                current_x += min_interval
            posList.append(rect_start)
            isSimpleList.append(False)
            
            ## right area - Check background complexity
            current_x = rect_end
            remain_length = border_removed_image.shape[1] - rect_end
            last_interval = min(remain_length % min_interval + min_interval, remain_length)
            k = max(math.floor((border_removed_image.shape[1] - rect_end - min_interval)/min_interval), 0)
            
            for _ in range(k):
                isSimpleList.append((detect_is_simple(shadow_edges, complexity_edges, current_x, current_x+min_interval)))
                posList.append(current_x)
                current_x += min_interval
            isSimpleList.append((detect_is_simple(shadow_edges, complexity_edges, current_x, current_x+last_interval)))
            posList.append(current_x)
            
            # 
            target_image = border_removed_image.copy()
            
            fill_start = None
            fill_flag = False
            fill_history = []
            print(posList)
            print(isSimpleList)
            for pos, isSimple in zip(posList, isSimpleList):
                if not fill_flag:
                    if not isSimple:
                        fill_start = pos
                        fill_flag = True
                else:
                    if isSimple:
                        target_image[:,fill_start:pos] = generate_gradient_image(target_image, fill_start, pos, expand_type=(True,False))
                        fill_history.append([fill_start, pos])
                        fill_flag = False
            if fill_flag:
                target_image[:,fill_start:] = generate_gradient_image(target_image, fill_start, expand_type=(True,False))
                fill_history.append([fill_start, target_image.shape[1]])
            cv2.imwrite(os.path.join('./images/SimpleNoblurred', basename + "_div." + extension), target_image)
            isLeftSimple, isRightSimple = SimpleExpander.is_simple(border_removed_image)
            json_data[basename] = {
                "fillHistory": fill_history,
                "isSimple": bool(isLeftSimple and isRightSimple)
            }
            
            # add original version
            target_image[:,fill_start:] = generate_gradient_image(border_removed_image, fill_start, expand_type=(True,False))
            cv2.imwrite(os.path.join('./images/SimpleNoblurred', basename + "_result." + extension), border_removed_image)
            
            
    with open('./images/SimpleNoblurred/simpleInfo.json', "w") as f:
        json.dump(json_data, f, indent=4)

