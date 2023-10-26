from rembg import remove
import numpy as np

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
