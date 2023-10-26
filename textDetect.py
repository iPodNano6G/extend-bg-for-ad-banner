import cv2
import numpy as np

def get_text_including_image(img):
    def non_max_suppression(boxes, scores, threshold):
        """
        Non-max suppression을 수행하여 겹치는 박스를 제거합니다.
        """
        if len(boxes) == 0:
            return []

        # 박스의 좌표를 풀어냅니다.
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        indexes = np.argsort(scores)
        keep = []

        while len(indexes) > 0:
            last = len(indexes) - 1
            i = indexes[last]
            keep.append(i)

            xx1 = np.maximum(x1[i], x1[indexes[:last]])
            yy1 = np.maximum(y1[i], y1[indexes[:last]])
            xx2 = np.minimum(x2[i], x2[indexes[:last]])
            yy2 = np.minimum(y2[i], y2[indexes[:last]])

            w = np.maximum(0, xx2 - xx1)
            h = np.maximum(0, yy2 - yy1)
            overlap = (w * h) / ((x2[i] - x1[i]) * (y2[i] - y1[i]) + (x2[indexes[:last]] - x1[indexes[:last]]) * (y2[indexes[:last]] - y1[indexes[:last]]) - w * h)

            indexes = np.delete(indexes, np.concatenate(([last], np.where(overlap > threshold)[0])))

        return keep

    # EAST 모델의 경로
    EAST_MODEL_PATH = 'frozen_east_text_detection.pb'
    image = img.copy()
    (h, w) = image.shape[:2]



    # 이미지의 크기를 조정합니다 (EAST 모델은 32의 배수로 크기를 조정하는 것을 선호합니다).
    (newW, newH) = (320, 320)
    rW = w / float(newW)
    rH = h / float(newH)
    image = cv2.resize(image, (newW, newH))

    # EAST 모델 로드
    net = cv2.dnn.readNet(EAST_MODEL_PATH)

    # 이미지를 모델에 전달하고 출력을 얻습니다.
    blob = cv2.dnn.blobFromImage(image, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])

    rects = []
    confidences = []
    # 각 탐지된 영역에 대해 상자를 그립니다.
    for i in range(0, scores.shape[2]):
        for j in range(0, scores.shape[3]):
            if scores[0, 0, i, j] < 0.5:
                continue
            
            # 출력에서 탐지된 텍스트 영역의 좌표를 추출합니다.
            (offsetX, offsetY) = (j * 4.0, i * 4.0)
            angle = geometry[0, 4, i, j]
            cos = np.cos(angle)
            sin = np.sin(angle)
            
            h = geometry[0, 0, i, j] + geometry[0, 2, i, j]
            w = geometry[0, 1, i, j] + geometry[0, 3, i, j]
            
            endX = int(offsetX + (cos * geometry[0, 1, i, j]) + (sin * geometry[0, 2, i, j]))
            endY = int(offsetY - (sin * geometry[0, 1, i, j]) + (cos * geometry[0, 2, i, j]))
            startX = int(endX - w)
            startY = int(endY - h)
            
            # 원래 이미지의 크기로 좌표를 조정합니다.
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)
            
            # 상자를 그립니다.
            #cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
            rects.append((startX, startY, endX, endY))
            confidences.append(scores[0, 0, i, j])

    indices = non_max_suppression(np.array(rects), np.array(confidences), 0.3)


    # NMS를 통해 선택된 상자만 그립니다.
    for i in indices:
        (startX, startY, endX, endY) = rects[i]
        print(rects[i])
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
    """    # rects[i]로 구한 영역을 추출
        roi = orig[startY:endY, startX:endX]
        # 해당 영역에 가우시안 블러 적용
        blurred_roi = cv2.GaussianBlur(roi, (199, 199), 0)
        # 블러 처리한 영역을 원래 이미지에 덮어씌움
        orig[startY:endY, startX:endX] = blurred_roi"""

    # 결과를 보여줍니다.
    cv2.imwrite("result3.jpg", orig)