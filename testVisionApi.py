"""
1. images/debug에 있는 모든 이미지 파일을 리스트로 만든다.(file_list, json_list)
2. (loop)이미지를 하나 선택하여 읽는다.
    1) 이미지 파일의 이름에 해당하는 data.json을 읽어 원본 공간을 투명 픽셀화 한다.
    2) api에 조작한 이미지를 넘겨서 object detection으로 결과를 추출한다.
    3) 리스트의 이미지 파일을 읽어 jsonList에 메타데이터를 추가시킨다.
        - 파일 이름(basename)
        - 감지된 오브젝트 dictionary 배열
            - name
            - score
            - ratio
    4) 조작한 이미지와 감지된 오브젝트를 직사각형으로 체크한 이미지를 만들어 images/debug/resultImage에 저장한다.
3. 모든 이미지 파일을 돌렸으면 objectDetection.json파일로 jsonList를 저장한다.

* 현재는 하나의 이미지에 대해 json파일 생성
"""


import os, re, cv2, json
import numpy as np
from utils.object_detector import ObjectDetector

# 환경 변수 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./secrets/google_key.json"


#loop 시작(아직 미구현)
object_array = []
#파일 읽기는 byte로
existing_image = next((filename for filename in os.listdir('.') if re.match(r'test\.(jpg|jpeg|png)$', filename)), None)#loop시 수정필요
with open(existing_image, "rb") as image_file:
    image_bytes = image_file.read()

#object detector 실행
results = ObjectDetector.detect_objects(image_bytes)

#직사각형 그리기
np_img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
h,w = np_img.shape[:2]
for object_dict in results:
    top = int(object_dict["top"]*h)
    bottom = int(object_dict["bottom"]*h)
    left = int(object_dict["left"]*w)
    right = int(object_dict["right"]*w)
    score = round(object_dict["score"]*100)
    occupancy_ratio = round(((bottom-top) * (right - left))/(h*w)*100, 2)
    object_array.append({
        "name" : object_dict["name"],
        "score": score,
        "ratio": occupancy_ratio
    })

    print(object_dict["name"] + f'({score}점): {occupancy_ratio}%')
    cv2.rectangle(np_img, (left, top), (right, bottom), (0,255,0), thickness = 2)
with open("apiResult.json", "w") as json_file:
    json.dump(object_array, json_file, indent=4)

cv2.imshow('Image with Rectangle', np_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("testResult.jpg", np_img)
