import os, cv2
import pandas as pd
import numpy as np
from openpyxl.drawing.image import Image
import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image

from skimage.feature import local_binary_pattern
from scipy.fft import fft2, fftshift

def extract_columns(foreground_removed_image: np.ndarray, n: int, side: str) -> np.ndarray:
    """
    Extracts n columns from the specified side of the background removed image while excluding transparent pixels.

    :param background_removed_image: The image with the background removed (includes alpha channel).
    :param n: The number of columns to extract.
    :param side: The side from which to extract the columns ('left' or 'right').
    :return: The extracted columns as an ndarray.
    """
    # Check if the image has an alpha channel
    if foreground_removed_image.shape[2] != 4:
        raise ValueError("The background removed image must have an alpha channel.")

    # Determine which columns to extract
    if side == 'left':
        cols = slice(n)
    elif side == 'right':
        cols = slice(-n, None)
    else:
        raise ValueError("Side must be 'left' or 'right'.")

    # Extract the alpha channel and determine where it's not transparent
    alpha_channel = foreground_removed_image[:, :, 3]
    non_transparent_mask = alpha_channel != 0

    # Initialize an array to hold the extracted columns
    extracted_columns = np.zeros((foreground_removed_image.shape[0], n, 3), dtype=foreground_removed_image.dtype)

    # Extract the columns while excluding transparent pixels
    for i in range(3):  # Iterate over the color channels (RGB)
        channel_data = foreground_removed_image[:, :, i]
        extracted_columns[:, :, i] = np.where(non_transparent_mask[:, cols], channel_data[:, cols], 0)

    return extracted_columns

# Method 1: Color Diversity Analysis using Color Histogram
def analyze_color_diversity(image: np.ndarray):
    # Calculate the color histogram
    histogram = cv2.calcHist([image], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    
    # Normalize the histogram
    histogram_normalized = cv2.normalize(histogram, histogram).flatten()

    # Calculate the entropy
    entropy = -np.sum(histogram_normalized * np.log2(histogram_normalized + 1e-9))
    
    return entropy

# Method 2: Texture Analysis using Edge Detection and Local Binary Pattern
def analyze_texture(image: np.ndarray):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Edge Detection
    edges = cv2.Canny(gray_image, 100, 200)
    edge_count = np.sum(edges > 0)
    
    # Local Binary Pattern
    lbp = local_binary_pattern(gray_image, P=8, R=1, method='uniform')
    lbp_hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 26), range=(0, 24))
    lbp_hist_normalized = lbp_hist / np.sum(lbp_hist)
    lbp_entropy = -np.sum(lbp_hist_normalized * np.log2(lbp_hist_normalized + 1e-9))
    
    return edge_count, lbp_entropy

# Method 3: Frequency Domain Analysis using Fourier Transform
def analyze_frequency_domain(image: np.ndarray):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Fourier Transform
    f_transform = fft2(gray_image)
    f_shifted = fftshift(f_transform)
    f_magnitude = 20 * np.log(np.abs(f_shifted))
    
    # Calculate the amount of high frequency components
    mean_frequency_amplitude = np.mean(f_magnitude)
    
    return mean_frequency_amplitude

def create_bg_only_image(original_image, background_removed_image):
    if original_image.shape[2] == 3:
        # Convert 3-channel image to 4-channel
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2BGRA)

    alpha_channel = background_removed_image[:, :, 3]
    mask = (alpha_channel < 128)
    bg_only_image = np.zeros_like(original_image)
    for i in range(3):
        bg_only_image[:, :, i] = np.where(mask, original_image[:, :, i], 0)
    bg_only_image[:, :, 3] = np.where(mask, 255, 0)

    return bg_only_image

def resize_image(img, target_height):
    """이미지를 높이에 맞게 비율을 유지하면서 리사이즈합니다."""
    # 원본 이미지의 비율을 계산
    ratio = img.width / img.height
    # 타겟 높이에 맞게 너비를 조정
    new_width = int(ratio * target_height)
    img.width, img.height = new_width, target_height
    return img




def process_images_to_excel2(original_dir, background_removed_dir, excel_path):
    # 워크북과 워크시트 생성
    wb = Workbook()
    ws = wb.active

    # 엑셀 헤더 설정
    ws.append([
        'product_id', 'original_image', 'background_removed_image',
        'entropy', 'edge_count', 'lbp_entropy', 'mean_frequency_amplitude'
    ])

    # List all files in the original images directory
    foreground_removed_image_folder = os.path.join(original_dir, "bg_only")
    if not os.path.isdir(foreground_removed_image_folder):
        os.mkdir(foreground_removed_image_folder)
    for filename in os.listdir(original_dir):
        if filename.endswith(".jpg"):
            product_id = os.path.splitext(filename)[0]
            original_image_path = os.path.join(original_dir, filename)

            background_removed_image_filename = f"{product_id}.png"
            background_removed_image_path = os.path.join(background_removed_dir, background_removed_image_filename)

            original_image = cv2.imread(original_image_path)
            background_removed_image = cv2.imread(background_removed_image_path, cv2.IMREAD_UNCHANGED)

            foreground_removed_image = create_bg_only_image(original_image, background_removed_image)
            extract_removed_image = extract_columns(foreground_removed_image, 5, "left")
            #분석 수행
            entropy = analyze_color_diversity(extract_removed_image)
            edge_count, lbp_entropy = analyze_texture(extract_removed_image)
            mean_frequency_amplitude = analyze_frequency_domain(extract_removed_image)

            # 이미지를 엑셀에 삽입
            img_original = Image(os.path.join(original_dir, filename))
            img_original = resize_image(img_original, 300)
            img_original.anchor = 'B' + str(ws.max_row + 1)  # 예를 들어 B2 셀에 배치
            ws.add_image(img_original)

            # Adjust the file extension for background removed images
            background_removed_image_filename = f"{product_id}.png"
            foreground_removed_image_path = os.path.join(foreground_removed_image_folder ,background_removed_image_filename)
            cv2.imwrite(foreground_removed_image_path, foreground_removed_image)
            img_foreground_removed = Image(foreground_removed_image_path)
            img_foreground_removed = resize_image(img_foreground_removed, 300)
            img_foreground_removed.anchor = 'C' + str(ws.max_row + 1)  # 예를 들어 C2 셀에 배치
            ws.add_image(img_foreground_removed)

            # 결과 데이터 추가
            ws.append([
                product_id,
                '',  # 이미지는 이미 삽입되었으므로 경로 대신 빈 문자열을 사용
                '',  # 이미지는 이미 삽입되었으므로 경로 대신 빈 문자열을 사용
                entropy, edge_count, lbp_entropy, mean_frequency_amplitude
            ])

    # Excel 파일 저장
    wb.save(excel_path)
# 사용 예
process_images_to_excel2(r'C:\projects\extend-bg-for-ad-banner\extract\border_removed_result',
         r"C:\projects\extend-bg-for-ad-banner\extract\border_removed_result\ps_background_removal2",
         "2023_11_08_complexity.xlsx")
