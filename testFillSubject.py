import cv2, os, re
from utils.border_remover import BorderRemover
from utils.foreground_remover import ForegroundRemover
from utils.dallE_filler import DallEFiller
from utils.mask_generator import MaskGenerator

if 'debug' not in os.listdir('./images'):
    os.mkdir('./images/debug')

for filename in os.listdir('./images/'): 
    if not re.match(r'^.+\.(jpg|jpeg|png)$', filename):
        continue

    print("Read", filename+"...")
    basename, extension = filename.split(".")[:2]
    if basename+"_result."+extension in os.listdir('./images/debug'):
        print(basename, "already exist")
        continue
    origin = cv2.imread(os.path.join('./images/', filename))
    origin = cv2.cvtColor(origin, cv2.COLOR_RGB2RGBA)

    borderRemovedImg, _ = BorderRemover.remove_border(origin)
    mask = MaskGenerator.load_mask("masks/", basename)

    subjectRemovedImg = ForegroundRemover.remove_subject(borderRemovedImg, mask)
    cv2.imwrite("removedSubject.jpg", subjectRemovedImg)
    prompt_text = "minimalistic photography on white background"
    filledImg = DallEFiller.fill_image(subjectRemovedImg, prompt_text=prompt_text)
    cv2.imwrite(os.path.join('./images/debug', basename+"_result."+extension),filledImg)
    with open('./images/debug/README.md', 'w') as readme_file:
        readme_file.write(prompt_text)