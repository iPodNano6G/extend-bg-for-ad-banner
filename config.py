#config.py

config = {
    #test
    "debug": False,
    "target_folder": "",#절대 경로 지정(기본값: /images)
    "process_single_file": False,#단일 파일 테스트 여부(batch mode or single mode)
    "batch_percentage": 1, # 1 = 100%
    "output_folder_name": "debug",#아웃풋 파일 명
    "mask_folder": "", #포토샵 배경제거 이미지가 들어 있는 곳


    #options
    "dallE_expand": True,
    "simple_expand": True,
    "remove_border": True, #테두리 제거 여부
    "add_white_border": False, #흰색 경계 추가 여부
    "divide_process": False, #분할 확장 여부
    "divide_parameter": 7, #분할 계수
    "prompt": "Extend background of Minimalist style whitespace photograph.", #프롬프트 지정
    "ratio": 2,
    # Extend background of Minimalistic style whitespace photography.
    "mask_generator": "photoshop", # 포토샵(phtoshop) or rembg
    "remove_subject": False, #피사체 제거 여부
    "dallE_fill": False, # DallE를 이용한 내부 이미지 추가
    "inner_prompt": "background of high-resolution photograph"
    #Dall-E키 값은 command argument로 받습니다.
    #batch mode
    # target_folder에 있는 모든 이미지 파일에 대해 batch_percentage만큼 추출하여 확장 후, 
    # target_folder 내에 output_folder_name이라는 폴더를 생성하여 그곳에 저장.

    #single mode
    #test.jpg 혹은 test.png 파일을 읽고, output_test.jpg 혹은 test_output.png, test_output.jpg로 저장
}

""" 
    보류 중인 테두리 알고리즘의 config
    "images_directory": "images",
    "mask_tool_options": ["rembg", "photoshop"],
    "default_mask_tool": "photoshop",
    #"default_mask_tool": "rembg",
    # 1 :using original mask area, 2: using rectangle area based on mask edge coordinate 
    "masked_area_options": ["origin", "rectangle"], 
    "default_masked_area": "origin", 
    # border edge detection low threshold
    "low_threshold": 5,
    # border edge detection high threshold
    "high_threshold": 25,
    # overlap threshold between mask and border
    "overlap_threshold": 2,
    # left, right expansion length(pixels)
    "left_expansion": 200,
    "right_expansion": 200,
    # dominant color threshold ratio
    "dominant_color_threshold_ratio": 0.4,
    # border_line ratio via width / height
    "border_line_threshold_ratio": 0.5,
    # border_line and edge minimum gap 
    "edge_buffer": 2,
    # expansion
    "top_expansion": 0, 
    "bottom_expansion": 0, 
    "left_expansion": 200, 
    "right_expansion": 200, 
    """