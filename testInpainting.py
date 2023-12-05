from utils.inpainter import Inpainter
import os

def convert_to_png_dir(path):
    png_path = os.path.splitext(path)[0] + '.png'
    return png_path


# 폴더 경로를 지정하세요 (예: 'C:/images/')
folder_path = r'C:\projects\extend-bg-for-ad-banner\extract\border_removed_result'
test_name = "inpainting_1"


test_path = os.path.join(folder_path, test_name)
if not os.path.exists(test_path):
    os.makedirs(test_path)

# 폴더 내의 모든 파일 목록을 가져옵니다
file_list = os.listdir(folder_path)
# 이미지 파일만 필터링합니다 (jpg, png, gif 등)
# 지원하는 이미지 파일 확장자
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
# 폴더 내의 파일들을 검색하고 이미지 파일만 리스트에 추가
image_files = []
for filename in os.listdir(folder_path):
    if any(filename.lower().endswith(ext) for ext in image_extensions):
        image_files.append(os.path.join(folder_path, filename))

for image_file_dir in image_files:
    file_name = os.path.basename(image_file_dir)
    result_path = os.path.join(test_path, file_name)
    result_path= convert_to_png_dir(result_path)
    print(image_file_dir)
    print(result_path)
    Inpainter.inpaint_using_ps(image_file_dir, result_path)