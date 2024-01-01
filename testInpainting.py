from utils.inpainter import Inpainter
import os, cv2

def find_object_box(image):
    # 투명 픽셀을 검출하기 위해 알파 채널을 추출
    alpha_channel = image[:, :, 3]

    # 알파 채널을 기반으로 피사체가 있는 영역의 좌표를 찾음
    non_zero_pixels = cv2.findNonZero(alpha_channel)
    left, top, width, height = cv2.boundingRect(non_zero_pixels)

    # 최소 크기의 직사각형의 좌표를 반환
    return left, top, left + width, top + height

def convert_to_png_dir(path):
    png_path = os.path.splitext(path)[0] + '.png'
    return png_path

# 폴더 경로를 지정하세요 (예: 'C:/images/')
folder_path = r'C:\projects\extend-bg-for-ad-banner\extract\border_removed_result'
mask_path = r"C:\projects\extend-bg-for-ad-banner\extract\border_removed_result\ps_background_removal2"
test_name = "(2023_12_21)generative_fill_square"

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
    product_code = os.path.splitext(os.path.basename(image_file_dir))[0]
    file_name = os.path.basename(image_file_dir)
    result_path = os.path.join(test_path, file_name)
    result_path= convert_to_png_dir(result_path)
    """
    mask_file_path = os.path.join(mask_path, product_code + ".png")
    mask_img = cv2.imread(mask_file_path, cv2.IMREAD_UNCHANGED)
    left, top, right, bottom = find_object_box(mask_img)
    mask_width = right - left
    mask_height = bottom - top
    height, width, _ = mask_img.shape
    if width - mask_width < width * 0.1 and height - mask_height < height * 0.1:
        pass
    else:
        Inpainter.content_aware_fill_square_using_ps(image_file_dir, result_path, top, bottom, left, right)
    """
    if os.path.exists(result_path):
        print("파일이 존재합니다.")
    else:
        Inpainter.generative_extend_using_ps(image_file_dir, result_path)