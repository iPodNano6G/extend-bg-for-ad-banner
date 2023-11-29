import requests, cv2
import numpy as np
from secret.api_key import api_keys
from utils.mask_generator import MaskGenerator
from utils.border_remover import BorderRemover


input_img = cv2.imread("test.jpg")
border_removed_img, _ = BorderRemover.remove_border(input_img)
_, buffer = cv2.imencode('.jpg', border_removed_img)
image_file_object = buffer.tobytes()

bg_removed_img = cv2.imread("mask.png", cv2.IMREAD_UNCHANGED)
mask_img = np.where(bg_removed_img[..., 3] >= 63, 0, 255).astype(np.uint8)
kernel = np.ones((10, 10), np.uint8)
eroded_mask = cv2.erode(mask_img, kernel, iterations=2)
inverted_mask = cv2.bitwise_not(eroded_mask)
cv2.imwrite("result.png", inverted_mask)

_, buffer = cv2.imencode('.png', inverted_mask)
mask_file_object = buffer.tobytes()

r = requests.post('https://clipdrop-api.co/cleanup/v1',
  files = {
    'image_file': ('test.jpg', image_file_object, 'image/jpg'),
    'mask_file': ('mask.png', mask_file_object, 'image/png')
    },
  headers = { 'x-api-key': api_keys['clipdrop']}
)
if (r.ok):
    with open("result.jpg", 'wb') as file:
        file.write(r.content)
else:
    r.raise_for_status()