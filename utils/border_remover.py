import cv2
import numpy as np
from config import config

print(config)
DEBUG = config["debug"]

class BorderRemover:
    def remove_border(img):
        return BorderRemoverV1.remove_border(img)


#케니 테두리 제거(보류)
class BorderRemoverV2:
    def __init__(self, config_data):
        self.config = config_data
        self.debug = config_data["debug"]
    def remove_border(self, img, mask, test_path="Canny.png"):
        edges = self.detect_edges(img)
        cv2.imwrite(test_path, edges)
        mask_edges = self.get_masked_area_coordinates(mask)
        results = self.find_first_border_lines(edges, mask_edges)
        
        #border_lines = results['border_lines']
        overlaps = results['overlaps']
        #diffs = results['diffs']
        final_border_lines = results['final_border_lines']
        
        isChopped = not all([overlap is True for overlap in overlaps.values()])
        croppedImg = self.remove_outside_borders(img, overlaps, final_border_lines)
        metaData = {
            "overlaps" : overlaps,#마스크와 
            "diffs" : results['diffs'],#마스크 경계와 감지된 엣지의 차이
            "final_border_lines" : final_border_lines,
            "isChopped" : isChopped
        }

        return croppedImg, metaData

    def detect_edges(self, img):
        """
        Detect edges in the given image using the Canny edge detection method.
        
        Parameters:
        - image_path (str): Path to the input image.
        - low_threshold (int): First threshold for the hysteresis procedure.
        - high_threshold (int): Second threshold for the hysteresis procedure.

        Returns:
        - edges (ndarray): Detected edges in the image.
        """
        low_threshold = self.config['low_threshold']
        high_threshold = self.config['high_threshold']

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(blurred, low_threshold, high_threshold)
        return canny

    def get_masked_area_coordinates(self, mask):
        """
        Return the coordinates (y, x) of the top, bottom, left, and right borders of the non-masked area.
        """
        y_indices, x_indices = np.where(mask == 0)  # 0 indicates the background in the mask.

        mask_edges = {
            'top': int(np.min(y_indices)),
            'bottom': int(np.max(y_indices)),
            'left': int(np.min(x_indices)),
            'right': int(np.max(x_indices))
        }

        return mask_edges

    def find_first_border_lines(self, edges, mask_edges):
        """
        Finds the border lines on the given edges image.
        1. border condition: border length / full border length > border threshold ratio
        2. minimum border coordinate: 1~3
        """
        threshold_ratio = self.config['border_line_threshold_ratio']
        edge_buffer = self.config.get('edge_buffer', 3)

        def find_border(data, threshold_ratio, max_index, reverse=False, continuous_threshold=2):
            total_threshold = int(threshold_ratio * len(data))
            continuous_compare_threshold = 0.10 * len(data)  # 연속조건 비교 임계값
            first_index = 0
            temporary_edge_count = 0  # 임시 변수로 edge_count 저장
            continuous_count = 0  # 연속적으로 나타나는 값의 개수를 세는 변수
            overlap = False # overlap 변수 초기화
            for index, line in enumerate(data):
                # max_index 넘어도 edge_buffer까지는 border line을 사용해서 이미지를 자르기로 하지만, mask와 overlap 은 된 것으로 판단하는 구간
                if index > max_index + edge_buffer:
                    overlap = True
                    break
                edge_count = np.sum(line == 255)
                if self.debug: 
                    print(f"Line index: {index}, Edge count: {edge_count}")

                # 연속조건 비교 임계값을 초과하는 경우
                if edge_count > continuous_compare_threshold:
                    # 첫 번째로 나타나는 경우
                    if continuous_count == 0:
                        temporary_edge_count = edge_count
                        continuous_count = 1
                    # 이전에 연속적으로 나타난 경우가 있는 경우
                    else:
                        temporary_edge_count += edge_count  # 임시 변수에 저장된 값과 현재 값을 더함
                        continuous_count += 1
                        if continuous_count >= continuous_threshold:
                            continuous_count = 0
                    first_index = index+1
                # 연속조건 비교 임계값을 넘지 않는 경우
                else:
                    continuous_count = 0
                    temporary_edge_count = 0
        
                # 연속적으로 나타난 값들의 합이 임계값을 초과하는 경우
                if temporary_edge_count > total_threshold:
                    if self.debug:
                        print(f"Threshold ratio: {threshold_ratio}, Threshold: {total_threshold}, temporary_edge_count:{temporary_edge_count}, Max index: {max_index}")
                    return (first_index if not reverse else data.shape[0] - first_index - 1, overlap)
        
            return (first_index if not reverse else data.shape[0] - first_index - 1, overlap)


        height, width = edges.shape

        # 각 방향에 대한 경계값 및 overlap 값을 반환받음
        top, top_overlap = find_border(edges, threshold_ratio, mask_edges['top'])
        bottom_data = edges[::-1]
        bottom, bottom_overlap = find_border(bottom_data, threshold_ratio, edges.shape[0] - mask_edges['bottom'] - 1, reverse=True)
        left, left_overlap = find_border(edges.T, threshold_ratio, mask_edges['left'])
        right_data = edges.T[::-1]
        right, right_overlap = find_border(right_data, threshold_ratio, edges.shape[1] - mask_edges['right'] - 1, reverse=True)

        # 경계선 조정 및 오버랩 체크 과정 포함
        overlap_threshold = self.config['overlap_threshold']
        overlaps = {
            'top': bool(top_overlap),
            'bottom':bool(bottom_overlap),
            'left': bool(left_overlap),
            'right': bool(right_overlap)
        }

        diffs = {}
        final_border_lines = {}

        diffs['top'], final_border_lines['top'] = self.compare_and_adjust_border('Top', mask_edges['top'], top, overlap_threshold)
        diffs['bottom'], final_border_lines['bottom'] = self.compare_and_adjust_border('Bottom', mask_edges['bottom'], bottom, overlap_threshold, reverse=True)
        diffs['left'], final_border_lines['left'] = self.compare_and_adjust_border('Left', mask_edges['left'], left, overlap_threshold)
        diffs['right'], final_border_lines['right'] = self.compare_and_adjust_border('Right', mask_edges['right'], right, overlap_threshold, reverse=True)

        return {
            'overlaps': overlaps,
            'mask_edges': mask_edges,
            'diffs': diffs,
            'border_lines': {
                'top': top if top is not None else 0,
                'bottom': bottom if bottom is not None else height,
                'left': left if left is not None else 0,
                'right': right if right is not None else width
            },
            'final_border_lines': final_border_lines
        }

    def compare_and_adjust_border(self, direction, mask_border, border, threshold, reverse=False, border_overlap=False):
        """
        Given the overlap status (`border_overlap`), this function will adjust the border if necessary.
        """
        # Return appropriate values if the border is None.
        if border is None:
            return None, None

        # Calculate the difference between mask_border and border based on the direction.
        diff = border - mask_border if reverse else mask_border - border

        # Determine the final border. If there's an overlap, the border remains the same. 
        # Otherwise, adjust it based on the difference and direction.
        if border_overlap: 
            final_border = border
        else:
            if reverse:
                final_border = int(max(border, mask_border)) if abs(diff) > threshold else min(border, mask_border)
            else:
                final_border = int(min(border, mask_border)) if abs(diff) > threshold else max(border, mask_border)

        if self.debug:
            pass
            #self.print_comparison(direction, border, mask_border, border_overlap, diff, final_border)

        return diff, final_border

    def remove_outside_borders(self, image, overlaps, border_lines):
            """
            Crop areas outside the border lines for non-overlapping directions.
            """
            y_start = 0 if overlaps['top'] else border_lines['top']
            y_end = image.shape[0] if overlaps['bottom'] else border_lines['bottom']
            x_start = 0 if overlaps['left'] else border_lines['left']
            x_end = image.shape[1] if overlaps['right'] else border_lines['right']
        
            return image[y_start:y_end, x_start:x_end]

#원래 사용하던 흰색 테두리 제거
class BorderRemoverV1:
    def add_border(img, border_size=100):
        # 이미지를 불러옵니다.
        # 테두리의 색을 흰색으로 설정합니다.
        white = [255, 255, 255, 255] if img.shape[2] == 4 else [255, 255, 255]

        # 이미지에 테두리를 추가합니다.
        bordered_img = cv2.copyMakeBorder(img, 
                                        top=border_size,
                                        bottom=border_size,
                                        left=border_size,
                                        right=border_size,
                                        borderType=cv2.BORDER_CONSTANT,
                                        value=white)
    
        return bordered_img
    def remove_border(img):
        bordered_img = BorderRemoverV1.add_border(img)
        # 그레이스케일 변환
        gray = cv2.cvtColor(bordered_img, cv2.COLOR_BGR2GRAY)
        # Gaussian 블러로 노이즈 제거
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Canny 엣지 디텍션
        edges = cv2.Canny(blurred, 5, 25)
        # 컨투어 찾기 
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 모든 컨투어를 하나로 병합
        merged_contour = np.vstack(contours)
        # 병합된 컨투어를 바탕으로 경계 사각형 찾기
        x, y, w, h = cv2.boundingRect(merged_contour)
        # 원본 이미지 크롭
        cropped_img = bordered_img[y:y+h, x:x+w]
        cropped_img = cropped_img[2:-2, 2:-2]
        if img.shape[0] == h and img.shape[1] == w:
            isChopped = False
        else:
            isChopped = True
        metaData = {
            "isChopped": isChopped
        }

        return cropped_img, metaData
