import cv2, requests, os, openai
import sys
from utils.dallE_expander import DallEExpander

class DallEFiller:
    testCount = 0
    def fill_image(img, prompt_text):
        height, width = img.shape[:2]
        result = None
        if height > width:
            #정사각형 만들기
            expand_length = int((height - width)/2)
            remainder = (height - width) % 2
            square_image = cv2.copyMakeBorder(img, 0, 0, expand_length+remainder, expand_length, cv2.BORDER_REPLICATE)
            #확장공간 블러링
            cpyLeft = square_image[:,:expand_length+remainder]
            blurLeft = cv2.blur(cpyLeft, (5,1), borderType = cv2.BORDER_REFLECT_101)
            square_image[:,:expand_length+remainder] = blurLeft
            if expand_length != 0:
                cpyRight = square_image[:,-expand_length:]
                blurRight = cv2.blur(cpyRight, (5,1), borderType = cv2.BORDER_REFLECT_101)
                square_image[:,-expand_length:] = blurRight
            input_image = cv2.resize(square_image, (1024,1024))

            #내부 채우기
            if len(sys.argv) == 2:
                output_image = DallEExpander.outpainting(input_image, key=sys.argv[1], length = 1024, prompt_text = prompt_text)
                cv2.imwrite(f"fillMediate{DallEFiller.testCount}.jpg", output_image)
                DallEFiller.testCount += 1
                output_image = cv2.resize(output_image, (height,height))
                # None으로 해놓지 않으면 0으로 잘라 버림
                result = output_image[:, expand_length+remainder:-expand_length if expand_length != 0 else None]
            else:
                return img
        elif width > height:
            raise RuntimeError("Need to add code!!")
        else:
            input_image = cv2.resize(img, (1024,1024))

            #내부 채우기
            if len(sys.argv) == 2:
                output_image = DallEExpander.outpainting(input_image, key=sys.argv[1], length = 1024, prompt_text = prompt_text)
                cv2.imwrite(f"fillMediate{DallEFiller.testCount}.jpg", output_image)
                DallEFiller.testCount += 1
                result = cv2.resize(output_image, (height, width))
            else:
                return img
        return result

