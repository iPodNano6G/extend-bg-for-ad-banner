from utils.mask_generator import MaskGenerator
from utils.border_touch_checker import BorderTouchChecker
from utils.paddingProcessor import PaddingProcessor
from utils.dallE_expander import DallEExpander

from utils.foreground_remover import ForegroundRemover
from utils.simple_expander import SimpleExpander
from utils.border_remover import BorderRemover
from utils.white_border_adder import WhiteBorderAdder


import cv2, os, random, json
import numpy as np

from config import config
#from text_detect import TextDetector
#from src.utils.image.image_bg_remover import ImageBgRemover

REMOVE_BORDER = config["remove_border"]
ADD_WHITE_BORDER = config["add_white_border"]
DIVIDE_PROCESS = config["divide_process"]


class ImageProcessor:
    def process_image(original_img, ratio = 2, expansion="unknown", key=""):
        # independent method on this class
        #original image: RGBA numpy
        origin_height, origin_width, _ = original_img.shape
        #1
        mask_img = MaskGenerator.make_mask(original_img)
        #cv2.imwrite("mask.png", mask_img) # 디버그용
        #2
        isLeft, isRight = False, False
        if(expansion == "unknown"):
            isLeft, isRight = BorderTouchChecker.check_mask_border(mask_img)
        if(expansion == "left"):
            isRight = True
        if(expansion == "right"):
            isLeft = True
        if(expansion == "both"):
            return original_img

        #3
        if isLeft and isRight:
            json_data = {
                "y_offset" : None,
                "x_offset" : None,
                "left_border_adjacent" : bool(isLeft),
                "right_border_adjacent" : bool(isRight)
            }
            return original_img, json_data
        padded_img, y_offset, x_offset = PaddingProcessor.addPadding(original_img, isLeft, isRight, ratio=ratio)
        #print(x_offset, y_offset)
        #cv2.imwrite("padded_img.png", padded_img) # 디버그용

        #3_resize
        resized_img = cv2.resize(padded_img, (1024, 1024))
        #cv2.imwrite("resized_img.png", resized_img)

        #4
        outpainted_img = DallEExpander.outpainting(resized_img, key=key)
        #cv2.imwrite("outpainted_img.png", outpainted_img)

        #4_resize
        recovered_img = cv2.resize(outpainted_img, (padded_img.shape[1], padded_img.shape[0]))
        #cv2.imwrite("recovered_img.png", recovered_img)

        #5
        recovered_img[y_offset:y_offset + origin_height, x_offset:x_offset+origin_width] = original_img
        #cv2.imwrite("original_composited_img.png", recovered_img)

        #6
        chopped_img = PaddingProcessor.chop_top_and_bottom(recovered_img, y_offset)
        #cv2.imwrite("chopped_img.png", chopped_img)

        json_data = {
            "y_offset" : int(y_offset*1024/padded_img.shape[0]),
            "x_offset" : int(x_offset*1024/padded_img.shape[1]),
            "left_border_adjacent" : bool(isLeft),
            "right_border_adjacent" : bool(isRight)
        }
        return chopped_img, json_data
    
    def single_process_image(image_path, save_path, key=""):
        # depend on "process_image"
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        bg_img = ForegroundRemover.remove_foreground(img)
        black_white, _ = SimpleExpander.determine_foreground_color(bg_img)

        base_name = os.path.basename(image_path)
        if black_white == "white":
            h, w, c = img.shape
            result = img
            
            result_path = os.path.join(save_path, black_white+ "_"+ base_name +".jpg")
        else:
            json_data = {}
            meta_data = {}
            expansion = "unknown"
            json_data = {
                "name" : str(base_name),
                "original_height" : int(img.shape[0]),
                "original_width" : int(img.shape[1])
            }
            border_removed_img = np.copy(img) #temp
            
            if REMOVE_BORDER:#sol1) 케니 테두리 제거 알고리즘
                #border_removed_img, isChopped = remove_border(img)
                temp_mask = MaskGenerator.make_mask(img)
                temp_path = os.path.join(save_path, "Canny_"+base_name)
                border_removed_img, meta_data = BorderRemover.remove_border(img)
                json_data.update(meta_data)
                pass
            if ADD_WHITE_BORDER:#sol2) 흰 테두리 추가 알고리즘(결과가 좋지 않았음)
                border_removed_img = WhiteBorderAdder.add_white_border(border_removed_img)
            
            if DIVIDE_PROCESS:
                border_removed_img, meta_data = ImageProcessor.process_image(border_removed_img,ratio=1.5, key=key)
                result_path = os.path.join(save_path, "intermediate" + ("_" if json_data["isChopped"] else "_unChopped_") + base_name)
                cv2.imwrite(result_path, border_removed_img)
                isLeft = meta_data["left_border_adjacent"]
                isRight = meta_data["right_border_adjacent"]
                if isLeft and isRight:
                    expansion = "both"
                else:
                    if isLeft:
                        expansion = "right"
                    elif isRight:
                        expansion = "left"

            result, meta_data = ImageProcessor.process_image(border_removed_img,ratio=2,expansion=expansion)#"left_border_adjacent", "right_border_adjacent" 속성 딕셔너리
            json_data.update(meta_data)
        result_path = os.path.join(save_path, "output" + ("_" if json_data["isChopped"] else "_unChopped_") + base_name)
        cv2.imwrite(result_path, result)
        return json_data

    def batch_process_images(folder_path, percentage=0.1, output_folder_name = "test_result", key=""):
        # depend on "single_process_image"
        # 지정된 폴더에서 모든 파일 목록을 가져옵니다.
        file_list = os.listdir(folder_path)

        # 이미지 파일만 추립니다.
        image_files = [f for f in file_list if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # 이미지 목록 중에서 20%를 랜덤으로 추출합니다.
        num_to_select = int(len(image_files) * percentage)
        selected_images = random.sample(image_files, num_to_select)
        
        #테스트 결과가 저장될 폴더 생성
        test_path = os.path.join(folder_path, output_folder_name)
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        # 선택된 이미지에 대해 작업을 수행합니다.
        json_list = []
        for file_name in selected_images:
            image_path = os.path.join(folder_path, file_name)
            print(image_path)
            
            json_data = ImageProcessor.single_process_image(image_path, test_path, key=key)
            json_list.append(json_data)
        with open(os.path.join(test_path, "data.json"), "w") as json_file:
            json.dump(json_list, json_file, indent=4)
            
