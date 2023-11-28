#test.py
import sys, os
from config import config
from processor.expand_processor import ImageProcessor

TARGET_FOLDER = config["target_folder"]
OUTPUT_FOLDER_NAME = config["output_folder_name"]

MASK_FOLDER = config["mask_folder"]

PROCESS_SINGLE_FILE = config["process_single_file"]
BATCH_PERCENTAGE = config["batch_percentage"]
PROMPT_TEXT = config["prompt"]
RATIO = config["ratio"]


if len(sys.argv) == 2:
    print("DallE key:", sys.argv[1])
    DALLE_KEY = sys.argv[1]
else:
    DALLE_KEY = ""

#1 마스크 생성
#2 마스크 경계인접 체크
#3 경계에 따라 패딩
#4 달리 확장
#5 원본 덮어쓰기
#6 위 아래 잘라내기

"""
아웃페인팅 서비스
인풋: 이미지
아웃풋: 1200*627 크기의 이미지
1. 원본 마스크 생성
    input: 원본 이미지(h*w)
    output: 원본 마스크(원본 사이즈)
2. 원본 마스크가 경계에 닿았는지 확인 (재구현)
    input: 원본 마스크 
    output: isLeft, isRight
3. 경계에 닿았는지에 따라, 이미지 주변에 투명 픽셀 추가
    input: 원본 이미지 
    output: paddedImage
4. 해당 이미지를 1024*1024로 리사이즈.
    input: paddedImage(padded_height, padded_width)
    output: resized_image 1024*1024
5. 이 이미지를 Dall-E에 보냄
    input: imageForDalle(1024*1024) 
    output: imageForDalle(1024*1024) 
6. 이 이미지를 투명픽셀을  포함한 사이즈로 리사이즈
    input: imageForDalle(1024*1024) 
    output: ResizedImage(padded_height*padded_width)
7. 이 위에 원본 배치
    input: ResizedImage(h*w), 원본 이미지 
    output: composited image(padded_height*padded_width), x_offset, yoffset
8. 위아래 잘라내기
    input: composited image(padded_height*padded_width), 
    

"""          

#
if TARGET_FOLDER == "":
    target_folder = os.path.join(os.getcwd(), "images/")#타겟 폴더 기본값: images
else:
    target_folder = TARGET_FOLDER
if MASK_FOLDER == "":
    mask_folder = os.path.join(os.getcwd(), "masks/")
else:
    mask_folder = MASK_FOLDER


"""
prompt_list = [
    " ",
    "Simply extend background.",
    "Simply extend background widely without any new objects or texts",
    "Simply extend monochromatic tone background widely without any new objects or texts.",
    "high-quality banner image.",
    "Minimalism style background.",
    "Minimalism style background without inroducing any new objects or texts.",
    "Wide-angle shot with ample whitespace",
    "Extend background of Minimalist style whitespace photography."
]
for idx, prompt_text in enumerate(prompt_list):
    ImageProcessor.batch_process_images(target_folder, output_folder_name= "promptTest"+str(idx), 
                                            mask_folder=mask_folder, percentage = BATCH_PERCENTAGE, 
                                            key=DALLE_KEY, prompt_text=prompt_text)
"""

#타겟 폴더(TARGET_FOLDER)의 이미지의 확장 결과를 아웃풋 폴더(OUTPUT_FOLDER_NAME)에 저장
if os.path.exists(os.path.join(target_folder, OUTPUT_FOLDER_NAME)):
    print(OUTPUT_FOLDER_NAME, "is already exist")
    exit()



if PROCESS_SINGLE_FILE:
    print(ImageProcessor.single_process_image(os.path.join(os.getcwd(), "test.jpg"), os.getcwd()), prompt=PROMPT_TEXT, key=DALLE_KEY)
else:
    ImageProcessor.batch_process_images(target_folder, ratio=RATIO, prompt_text=PROMPT_TEXT, output_folder_name=OUTPUT_FOLDER_NAME, mask_folder=mask_folder, percentage = BATCH_PERCENTAGE, key=DALLE_KEY)