import cv2

#인위적으로 하얀색 경계 추가
class WhiteBorderAdder:
    def add_white_border(image, width = 100):
        """
        Add a white border to the top and bottom of the image.

        Parameters:
        - image: np.array, the input image.
        - top: int, the width of the border to be added to the top of the image.
        - bottom: int, the width of the border to be added to the bottom of the image.

        Returns:
        - np.array: the image with the added borders.
        """
        # Define the color of the border [B, G, R]
        color = [255, 255, 255]

        # Add the border
        bordered_image = cv2.copyMakeBorder(image, width, width, 0, 0, cv2.BORDER_CONSTANT, value=color)

        return bordered_image
