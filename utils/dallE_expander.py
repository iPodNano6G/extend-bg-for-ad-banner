import cv2, requests, os
from openai import OpenAI
import numpy as np


class DallEExpander:
    def download_image(url, folder_path = '.', file_name = "downloaded_image.png"):
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(folder_path, exist_ok=True)
            image_path = folder_path+"/"+file_name
            with open(image_path, 'wb') as file:
                file.write(response.content)
            return os.path.normpath(os.path.abspath(image_path))
        else:
            print(response.status_code)
    
    def outpainting(np_image, key="", length = 1024, prompt_text = " ") -> 'np.ndarray': 
        resized_image = cv2.resize(np_image, (length, length))
        print("프롬프트: [" + prompt_text + "]")
        if key == "":
            print("DALLE outpainting을 생략합니다")
            return resized_image
        client = OpenAI(api_key=key)
        #cv2.imwrite("outpainting_temp.png", resized_image)[1].tobytes()
        encoded_img = cv2.imencode('.png', np_image)[1].tobytes()
        response = client.images.edit(
            #prompt="photo of person",
            #1. Simply extend background without introducing any new objects or texts.
            #2. high-quality banner image
            #3. high-quality background
            #4. extend as computer wallpaper
            #9: 
            model="dall-e-2",
            image=encoded_img,
            mask=encoded_img,
            prompt=prompt_text,
            n=1,
            size= str(length)+"x"+str(length)
        )
        image_url = response.data[0].url

        dallE_image_path = DallEExpander.download_image(image_url, file_name = "dallE.png")
        dallE_np_image = cv2.imread(dallE_image_path)
        dallE_np_image = cv2.cvtColor(dallE_np_image,cv2.COLOR_RGB2RGBA)

        return dallE_np_image