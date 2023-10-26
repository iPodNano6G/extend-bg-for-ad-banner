import numpy as np

class BorderTouchChecker:
    def check_mask_border(mask_img, threshold=1):
        unique_values = np.unique(mask_img)
        if not np.array_equal(unique_values, [0, 1]) and not np.array_equal(unique_values, [0, 255]):
            raise ValueError("The mask should be a binary image with values 0 and 1 or 0 and 255")

        # Check the first and last column
        left_border = mask_img[:, 0]
        right_border = mask_img[:, -1]
        
        # Check if there are white pixels in the first or last column
        touch_left = np.sum(left_border == 0) >= threshold
        touch_right = np.sum(right_border == 0) >= threshold
        
        return touch_left, touch_right 
