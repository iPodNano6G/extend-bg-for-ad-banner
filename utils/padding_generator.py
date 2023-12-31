import numpy as np

#패딩 추가 및 추가한 패딩 공간 잘라내기
class PaddingGenerator:
    def addPadding(np_image, left=False, right=False, ratio = 2)->"np.darray, int, int":
        h, w, c = np_image.shape
        expand_direction = None
        result_length = None
        if w/h > ratio:
            expand_direction = 'vertical'
            if ratio <= 1:
                x = int((1/ratio-1)*w/2)#정사각형을 만들기 위한 공간
                result_length = int(w/ratio)
            else:
                x = 0
                result_length = w
            #y_offset
            y = int((w/ratio-h)/2)
        else:
            expand_direction = 'horizontal'
            if ratio >= 1:
                y = int((ratio-1)*h/2)#정사각형을 만들기 위한 공간
                result_length = int(ratio*h)
            else:
                y = 0
                result_length = h
            #x_offset
            if left and right:
                return None
            elif left:
                x = 0
            elif right:
                x = int(ratio*h-w)
            else:
                x = int((ratio*h-w)/2)
        result = np.zeros((result_length, result_length, 4), dtype=np.uint8)
        result[y:y+h, x:x+w] = np_image
        
        return result, y, x, expand_direction
    def chop_top_and_bottom(img, y1, y2):
        chopped_img = img[y1:y2, :]
        return chopped_img
    def chop_left_and_right(img, x1, x2):
        chopped_img = img[:, x1:x2]
        return chopped_img
