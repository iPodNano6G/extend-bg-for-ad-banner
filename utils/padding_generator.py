import numpy as np

#패딩 추가 및 추가한 패딩 공간 잘라내기
class PaddingGenerator:
    def addPadding(np_image, left=False, right=False, ratio = 2)->"np.darray, int, int":
        h, w, c = np_image.shape
        if w/h > ratio:
            return None
        if ratio < 1:
            ratio = 1
        y = int((ratio-1)*h/2)
        if left and right:
            return None
        elif left:
            x = 0
        elif right:
            x = int(ratio*h-w)
        else:
            x = int((ratio*h-w)/2)
        result = np.zeros((int(ratio*h), int(ratio*h), 4), dtype=np.uint8)
        print(x, result.shape, np_image.shape)
        result[y:y+h, x:x+w] = np_image
        
        return result, y, x
    def chop_top_and_bottom(img, h1, h2):
        chopped_img = img[h1:h2, :]
        return chopped_img
