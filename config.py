#config.py

config = {
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

    #test
    "debug": False,
    "target_folder": "",#절대 경로 지정
    "process_single_file": False,#단일 파일 테스트 여부
    "batch_percentage": 1, # 1 -> 100% 0.2 -> 20%
    "output_folder_name": "labeling_10_26_divideprocess",#아웃풋 파일 명

    #options
    "remove_border": True,
    "add_white_border": False,
    "divide_process": True,
}
