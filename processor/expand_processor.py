from utils.mask_generator import MaskGenerator
from utils.border_touch_checker import BorderTouchChecker
from utils.padding_generator import PaddingGenerator
from utils.dallE_expander import DallEExpander

from utils.foreground_remover import ForegroundRemover
from utils.simple_expander import SimpleExpander
from utils.border_remover import BorderRemover
from utils.dallE_filler import DallEFiller
from utils.white_border_adder import WhiteBorderAdder


import cv2, os, random, json, time, re
import numpy as np

from config import config
#from text_detect import TextDetector
#from src.utils.image.image_bg_remover import ImageBgRemover

DALLE_EXPAND = config["dallE_expand"]

REMOVE_BORDER = config["remove_border"]
ADD_WHITE_BORDER = config["add_white_border"]
DIVIDE_PROCESS = config["divide_process"]

MASK_GENERATOR = config["mask_generator"]
REMOVE_SUBJECT = config["remove_subject"]
DALLE_FILL = config["dallE_fill"]


class ImageProcessor:
    def process_image(input_img, ratio = 2, test_info=None):
        # input_img should always be RGBA np image
        # ratio: ratio(weight/height) of the result image

        # test_info : dictionary argument for process status
        # "basename", "mask_folder", "expansion", "key"
        origin_height, origin_width, _ = input_img.shape
        #1 마스크 생성
        if(MASK_GENERATOR == "photoshop"):
            mask_img = MaskGenerator.load_mask(test_info["mask_folder"], test_info["basename"])
        else:
            mask_img = MaskGenerator.make_mask(input_img)
        #2 경계 판단
        isLeft, isRight = False, False
        expansion = test_info["expansion"]
        if(expansion == "unknown"):
            isLeft, isRight = BorderTouchChecker.check_mask_border(mask_img)
        if(expansion == "left"):
            isRight = True
        if(expansion == "right"):
            isLeft = True
        if(expansion == "both"):
            return input_img

        if isLeft and isRight:
            json_data = {
                "Dall_E_y_offset" : None,
                "Dall_E_x_offset" : None,
                "x_offset" : 0,
                "y_offset" : 0,
                "left_border_adjacent" : bool(isLeft),
                "right_border_adjacent" : bool(isRight)
            }
            return input_img, json_data
        
        ImgForPadding = input_img
        #3 내부를 DallE로 채우는 로직
        if DALLE_FILL:
            kernel_size = 10
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            eroded_mask = cv2.erode(mask_img, kernel, iterations=1)
            subjectRemovedImg = ForegroundRemover.remove_subject(input_img, eroded_mask)
            prompt_text = config["inner_prompt"]# filling prompt
            ImgForPadding = DallEFiller.fill_image(subjectRemovedImg, prompt_text=prompt_text)

        #4 특정 비율로 이미지 확장 영역 확보
        result_tuple = PaddingGenerator.addPadding(ImgForPadding, isLeft, isRight, ratio=ratio)
        if result_tuple == None:# 원본 이미지가 이미 1:2 비율을 초과한 경우
            json_data = {
                "Dall_E_y_offset" : None,
                "Dall_E_x_offset" : None,
                "x_offset" : 0,
                "y_offset" : 0,
                "left_border_adjacent" : bool(isLeft),
                "right_border_adjacent" : bool(isRight)
            }
            return input_img, json_data
        padded_img, y_offset, x_offset = result_tuple


        #5 DallE를 위한 1024*1024 비율 조절
        resized_img = cv2.resize(padded_img, (1024, 1024))

        #6 DallE api를 통해 확장
        if DALLE_EXPAND:
            outpaint_time = time.time()
            try:
                outpainted_img = DallEExpander.outpainting(resized_img, key=test_info["key"], prompt_text=test_info["prompt"])
            except Exception as e:
                print(e)
                print("10초 후 한번 더 시도합니다.")
                time.sleep(10)
                try:
                    outpainted_img = DallEExpander.outpainting(resized_img, key=test_info["key"], prompt_text=test_info["prompt"])
                except Exception as e:
                    print(e)
                    print("Dall-E 모델 에러, 프로그램을 종료합니다.")
                    exit()
            print("Dall-E time: ", time.time() - outpaint_time)
        else:
             outpainted_img = resized_img

        #7 원본 비율 복구
        recovered_img = cv2.resize(outpainted_img, (padded_img.shape[1], padded_img.shape[0]))

        #8 확장 정보 저장
        json_data = {
            "prompt" : test_info["prompt"],
            "x_offset" : x_offset,#결과물에서 원본 사진의 좌표
            "y_offset" : y_offset,
            "Dall_E_y_offset" : int(y_offset*1024/padded_img.shape[0]),#달리 input에서 원본 사진의 좌표
            "Dall_E_x_offset" : int(x_offset*1024/padded_img.shape[1]),
            "left_border_adjacent" : bool(isLeft),#경계선 인접 정보
            "right_border_adjacent" : bool(isRight)
        }

        return recovered_img, json_data
    
    def single_process_image(image_path, prompt_text, save_path="", mask_folder="masks", key=""):
        test_info = {
            # 공백 또는 언더바를 제외한 앞의 코드를 basename으로 정한다.
            "basename": re.split(r'\s+|_', os.path.splitext(os.path.basename(image_path))[0])[0],
            "mask_folder": mask_folder,
            "expansion": "unknown",
            "key": key,
            "prompt": prompt_text
        }

        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        bg_img = ForegroundRemover.remove_foreground(img)# deprecated: 새로운 단색 판단 알고리즘 적용 필요
        black_white, _ = SimpleExpander.determine_foreground_color(bg_img)# deprecated: 새로운 단색 판단 알고리즘 적용 필요

        base_name = os.path.basename(image_path)
        base_id, extention = os.path.splitext(base_name)
        json_data = {}
        if black_white == "white":# deprecated: 새로운 단색 판단 알고리즘 적용 필요
            h, w, c = img.shape
            final_img = img
            
            result_path = os.path.join(save_path, black_white+ "_"+ base_name)
            json_data = {
                "name" : str(base_name),
                "original_height" : int(img.shape[0]),
                "original_width" : int(img.shape[1]),
                "isChopped" : False
            }
        else:
            meta_data = {}#method에서 불러올 meta data
            json_data = {#확장 과정 중 발생한 metadata
                "name" : str(base_name),
                "original_height" : int(img.shape[0]),
                "original_width" : int(img.shape[1])
            }
            temp_img = img.copy() #temp
            
            if REMOVE_BORDER:# 개선 필요
                temp_img, meta_data = BorderRemover.remove_border(temp_img)
                json_data = {
                    "name" : str(base_name),
                    "original_height" : int(temp_img.shape[0]),
                    "original_width" : int(temp_img.shape[1])
                }
                json_data.update(meta_data)
                
            if REMOVE_SUBJECT:
                mask = MaskGenerator.load_mask(test_info["mask_folder"], test_info["basename"])
                temp_img = ForegroundRemover.remove_subject(temp_img, mask_img=mask)
            
            if DIVIDE_PROCESS:
                img_height, img_width = temp_img.shape[:2]
                r = float(img_width) / img_height
                k = config["divide_parameter"]
                expand_ratio = r*(k+2)/k
                if expand_ratio >= 2:
                    json_data["expand_ratio"] = None
                    print("No need to divide")
                else:
                    print("expand ratio: ", expand_ratio)
                    json_data["expand_ratio"] = expand_ratio
                    temp_img, meta_data = ImageProcessor.process_image(temp_img,ratio=2, test_info=test_info)
                    print([img_height, img_width], "to", temp_img.shape[:2])
                    result_path = os.path.join(save_path, base_id + "_inter" + ("_unChopped" if not json_data["isChopped"] else "") + extention)
                    cv2.imwrite(result_path, temp_img)
                    isLeft = meta_data["left_border_adjacent"]
                    isRight = meta_data["right_border_adjacent"]
                    if isLeft and isRight:
                        test_info["expansion"] = "both"
                    else:
                        if isLeft:
                            test_info["expansion"] = "right"
                        elif isRight:
                            test_info["expansion"] = "left"

            DallE_result, meta_data = ImageProcessor.process_image(temp_img, ratio=2, test_info=test_info)#"left_border_adjacent", "right_border_adjacent" 속성 딕셔너리
            cv2.imwrite(os.path.join(save_path, "DallE/", base_id+"_DALLE"+extention), DallE_result)
            
            # 원본 복구
            y_offset = meta_data["y_offset"]
            x_offset = meta_data["x_offset"]
            origin_height, origin_width = temp_img.shape[:2]
            DallE_result[y_offset : y_offset + origin_height, x_offset : x_offset + origin_width] = temp_img

            # 불필요한 이미지 제거
            final_img = PaddingGenerator.chop_top_and_bottom(DallE_result, y_offset, y_offset + origin_height)

            json_data.update(meta_data)
        result_path = os.path.join(save_path, base_id+ "_output" + ("_unChopped" if not json_data["isChopped"] else "") + extention)
        cv2.imwrite(result_path, final_img)
        return json_data

    def batch_process_images(input_path, prompt_text, mask_folder="masks", percentage=0.1, output_folder_name = "test_result", key=""):
        # depend on "single_process_image"
        # 지정된 폴더에서 모든 파일 목록을 가져옵니다.
        file_list = os.listdir(input_path)

        # 이미지 파일만 추립니다.
        image_files = [f for f in file_list if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # 이미지 목록 중에서 20%를 랜덤으로 추출합니다.
        num_to_select = int(len(image_files) * percentage)
        selected_images = random.sample(image_files, num_to_select)
        
        #테스트 결과가 저장될 폴더 생성
        save_path = os.path.join(input_path, output_folder_name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            os.makedirs(os.path.join(save_path, "DallE/"))
        with open(os.path.join(save_path, "config.md"),"w") as readme_file:
             readme_file.write(json.dumps(config, indent=4))
        # 선택된 이미지에 대해 작업을 수행합니다.
        json_list = []
        for file_name in selected_images:
            image_path = os.path.join(input_path, file_name)
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
            json_data = ImageProcessor.single_process_image(image_path, save_path=save_path, mask_folder=mask_folder, key=key, prompt_text=prompt_text)
            json_list.append(json_data)
        json_list.append(config)
        with open(os.path.join(save_path, "data.json"), "w") as json_file:
            json.dump(json_list, json_file, indent=4)
            
