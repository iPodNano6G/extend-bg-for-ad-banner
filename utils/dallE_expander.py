import cv2, requests, os, openai
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
    
    def outpainting_using_DallE2(np_image, prompt_text, length = 1024, dalle_key="") -> 'np.ndarray': 
        resized_image = cv2.resize(np_image, (length, length))
        print("프롬프트: [" + prompt_text + "]")
        if dalle_key == "":
            print("DALLE outpainting을 생략합니다")
            return resized_image
        openai.api_key = dalle_key


        cv2.imwrite("outpainting_temp.png", resized_image)
        outpainted = openai.Image.create_edit(
        image = open("outpainting_temp.png", "rb"),
            #prompt="photo of person",
            #1. Simply extend background without introducing any new objects or texts.
            #2. high-quality banner image
            #3. high-quality background
            #4. extend as computer wallpaper
            #9: 

            prompt=prompt_text,
            n=1,
            size= str(length)+"x"+str(length)
        )
        image_url = outpainted.data[0]['url']

        dallE_image_path = DallEExpander.download_image(image_url, file_name = "dallE.png")
        dallE_np_image = cv2.imread(dallE_image_path)
        dallE_np_image = cv2.cvtColor(dallE_np_image,cv2.COLOR_RGB2RGBA)

        return dallE_np_image

    def outpainting_using_DallE3(np_image, length = 1024, dalle_key="") -> 'np.ndarray': 
        pass

    def outpainting(np_image, key="", prompt_text = " ") -> 'np.ndarray':
        return DallEExpander.outpainting_using_DallE2(np_image, dalle_key=key, prompt_text=prompt_text)