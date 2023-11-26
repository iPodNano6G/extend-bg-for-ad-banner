from rembg import remove
import numpy as np
import cv2, os

class MaskGenerator:
    def make_mask_using_rembg(np_img):
        bg_removed_np_image = remove(np_img)
        #cv2.imwrite("bg_removed.png", bg_removed_np_image)
        mask_img = np.where(bg_removed_np_image[..., 3] >= 127, 0, 255).astype(np.uint8)
        return mask_img

    def make_mask_using_photoshop(np_img):
        pass

    def make_mask(np_img):
        mask_img = MaskGenerator.make_mask_using_rembg(np_img)
        return mask_img
    
    def load_mask(mask_folder, basename):
        files = os.listdir(mask_folder)
        for file_name in files:
            if basename in file_name:
                # 피사체는 검은색, 객체는 흰색 (h,w)
                bg_removed_np_image = cv2.imread(os.path.join(mask_folder, file_name), cv2.IMREAD_UNCHANGED)
                mask_img = np.where(bg_removed_np_image[..., 3] >= 63, 0, 255).astype(np.uint8)
                #cv2.imwrite("mask.png", mask_img)
                return mask_img
        raise RuntimeError("No such mask file")
    
