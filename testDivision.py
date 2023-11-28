#testDivision.py
import sys, os, cv2, json
import numpy as np
from service.expand_service import ExpandService
from utils.border_remover import BorderRemover
from config import config


if len(sys.argv) == 2:
    print("DallE key:", sys.argv[1])
    DALLE_KEY = sys.argv[1]
else:
    DALLE_KEY = ""

#
target_folder = os.path.join(os.getcwd(), "images/")#타겟 폴더 기본값: images
mask_folder = os.path.join(os.getcwd(), "masks/")


#타겟 폴더(TARGET_FOLDER)의 이미지의 확장 결과를 아웃풋 폴더(OUTPUT_FOLDER_NAME)에 저장
if os.path.exists(os.path.join(target_folder, "multiple-expansion")):
    print("multiple-expansion", "is already exist")
    exit()

save_path = os.path.join(target_folder, "divTest/")
file_list = os.listdir(target_folder)


# 이미지 파일만 추립니다.
image_files = [f for f in file_list if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

#테스트 결과가 저장될 폴더 생성
if not os.path.exists(save_path):
    os.makedirs(save_path)


def single_process_image_forDiv(image_path, prompt_text, save_path="", mask_folder="masks", key=""):
    test_info = {
        "basename": (os.path.splitext(os.path.basename(image_path))[0]).split()[0],
        "mask_folder": mask_folder,
        "expansion": "unknown",
        "key": key,
        "prompt": prompt_text
    }

    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

    base_name = os.path.basename(image_path)
    base_id, extention = os.path.splitext(base_name)
    json_data = {}
    meta_data = {}
    json_data = {
        "name" : test_info["basename"],
        "original_height" : int(img.shape[0]),
        "original_width" : int(img.shape[1])
    }
    border_removed_img = np.copy(img) #temp
    
    border_removed_img, meta_data = BorderRemover.remove_border(img)
    json_data.update(meta_data)

    # DIVIDE_PROCESS
    img_height, img_width = border_removed_img.shape[:2]
    expand_ratio = float(img_width) / img_height
    idx = 0
    while(expand_ratio < 2):
        expand_ratio *= 9/7
        if expand_ratio >= 2:
            expand_ratio = 2
        print(str(idx+1)+"번째, " + "expand ratio: ", expand_ratio)
        json_data["expand_ratio"] = expand_ratio
        prev_h, prev_w = border_removed_img.shape[:2]
        border_removed_img, meta_data = ExpandService.process_image(border_removed_img,ratio=expand_ratio, test_info=test_info)
        print((prev_h, prev_w), "to", border_removed_img.shape[:2])
        if expand_ratio == 2: 
            result_path = os.path.join(save_path, base_id + "_last" + ("_unChopped" if not json_data["isChopped"] else "") + extention)
        else:
            result_path = os.path.join(save_path, base_id + "_inter" + str(idx+1) + ("_unChopped" if not json_data["isChopped"] else "") + extention)
        
        isLeft = meta_data["left_border_adjacent"]
        isRight = meta_data["right_border_adjacent"]
        if isLeft and isRight:
            test_info["expansion"] = "both"
        else:
            if isLeft:
                test_info["expansion"] = "right"
            elif isRight:
                test_info["expansion"] = "left"
        inter_img = np.copy(border_removed_img)
        cv2.line(inter_img, (meta_data["x_offset"],0),(meta_data["x_offset"],inter_img.shape[0]), (0,255,0))
        if isRight: 
            cv2.line(inter_img, (inter_img.shape[1]-1,0),(inter_img.shape[1]-1,inter_img.shape[0]),(0,255,0))
        else:
            cv2.line(inter_img, (inter_img.shape[1]-(meta_data["x_offset"]+1),0),(inter_img.shape[1]-(meta_data["x_offset"]+1),inter_img.shape[0]),(0,255,0))
        cv2.imwrite(result_path, inter_img)
        idx+=1

    json_data.update(meta_data)
    result_path = os.path.join(save_path, base_id+ "_output" + ("_unChopped" if not json_data["isChopped"] else "") + extention)
    cv2.imwrite(result_path, border_removed_img)
    return json_data


# 선택된 이미지에 대해 작업을 수행합니다.
json_list = []
for file_name in image_files:
    image_path = os.path.join(target_folder, file_name)
    print(image_path)
    #save_path에 이미 파일이 있는지 확인
    saved_list = os.listdir(save_path)
    flag = 0
    for saved_file in saved_list:
        if os.path.splitext(file_name)[0] in saved_file:
            print(saved_file, "already exist")
            flag = 1
            break
    if flag == 1:
        continue
    json_data = single_process_image_forDiv(image_path, save_path=save_path, mask_folder=mask_folder, key=DALLE_KEY, prompt_text=config["prompt"])
    json_list.append(json_data)
with open(os.path.join(save_path, "data.json"), "w") as json_file:
    json.dump(json_list, json_file, indent=4)
 
 