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

현재 코드가 매우 지저분하므로 추후 정리 필요
"""


import os, re, cv2, json
import numpy as np
from utils.object_detector import ObjectDetector

# 환경 변수 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./secrets/google_key.json"


#loop 시작(아직 미구현)
json_list = []
meta_data = None#basename, x_offset 등이 담겨 있는 dictionary들의 리스트
with open(os.path.join(os.getcwd(), "images/debug/", "data.json"), "r") as json_file:
    meta_data = json.load(json_file)

if not isinstance(meta_data, list):
    print("Failed to read data.json")
    exit(0)

os.mkdir('./images/debug/objectDetection/')

for filename in os.listdir('./images/debug/'): 
    if not re.match(r'^.+\.(jpg|jpeg|png)$', filename):
        continue
    print("Read", filename+"...")
    basename = filename.split("_")[0]
    x_offset, y_offset, w, h = None, None, None, None
    for image_data in meta_data:
        if basename in image_data["name"]:
            if "x_offset" not in image_data:
                print("Failed----\n", image_data)
                break
            x_offset = image_data["x_offset"]
            y_offset = image_data["y_offset"]
            w = image_data["original_width"]
            h = image_data["original_height"]
            break
    if x_offset == None:
        print("Failed to find", basename)
        continue
    
    expanded_image = cv2.imread(os.path.join('./images/debug/', filename))
    expanded_image = cv2.cvtColor(expanded_image, cv2.COLOR_RGB2RGBA)
    print(expanded_image.shape, y_offset, x_offset)
    print(y_offset, y_offset+h, x_offset, x_offset+w)
    print((h,w,4))
    #추후 확장성을 위해 정확한 좌표 처리 필요
    # 현재 data.json의 original_width값이 부정확함, x_offset값 등 정확한지 검증이 필요
    mask = np.zeros((min(h, expanded_image.shape[0]),w,4), dtype=np.uint8)
    expanded_image[:h, x_offset:x_offset+w] = mask
    image_bytes = cv2.imencode('.jpg', expanded_image)[1].tobytes()

    objectResults = ObjectDetector.detect_objects(image_bytes)
    textResults, fullText = ObjectDetector.detect_texts(image_bytes)

    #직사각형 그리기
    h,w = expanded_image.shape[:2]
    object_array = []
    text_array = []
    for object_dict in objectResults:
        if object_dict["name"] != 'person':
            continue
        top = int(object_dict["top"]*h)
        bottom = int(object_dict["bottom"]*h)
        left = int(object_dict["left"]*w)
        right = int(object_dict["right"]*w)
        score = round(object_dict["score"]*100)
        occupancy_ratio = round(((bottom-top) * (right - left))/(h*w)*100, 2)
        object_array.append({
            "score": score,
            "ratio": occupancy_ratio
        })

        print(f'({score}점): {occupancy_ratio}%')
        cv2.rectangle(expanded_image, (left, top), (right, bottom), (0,255,0), thickness = 2)
        cv2.putText(expanded_image, object_dict["name"], (left, top+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2, cv2.LINE_AA, False)
    
    for text_dict in textResults:
        top = int(text_dict["top"])
        bottom = int(text_dict["bottom"])
        left = int(text_dict["left"])
        right = int(text_dict["right"])
        occupancy_ratio = round(((bottom-top) * (right - left))/(h*w)*100, 2)
        text_array.append({
            "description" : text_dict["description"],
            "ratio": occupancy_ratio
        })

        print(text_dict["description"] + f'(: {occupancy_ratio}%')
        cv2.rectangle(expanded_image, (left, top), (right, bottom), (255,0,0), thickness = 2)
    
    print(os.path.join('./images/debug/objectDetection/'+basename+'_object.jpg'))
    cv2.imwrite(os.path.join('./images/debug/objectDetection/'+basename+'_object.jpg'), expanded_image)
    json_list.append({"name": basename, "person": object_array, "description": fullText, "text": text_array})
json_list.sort(key=lambda x: x['name'])
with open('./images/debug/objectDetection/objectDetection.json', "w") as json_file:
    json.dump(json_list, json_file, indent=4)


"""signle

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
with open("objectDetection.json", "w") as json_file:
    json.dump(object_array, json_file, indent=4)

cv2.imshow('Image with Rectangle', np_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("testResult.jpg", np_img)
"""