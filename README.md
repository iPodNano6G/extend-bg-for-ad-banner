# 통합 테스트 시스템 실행 방법
0. 필요한 패키지를 설치 및 구글 api key 등록
 - pip install rembg
 - pip install openai
 - secrets/google_key.json

1. config.py를 목적에 맞게 설정한다.
2. "images/" 혹은 사용자 지정 위치에 테스트할 샘플 이미지 파일을 넣는다.
3. 포토샵 배경 제거를 이용하는 경우, "masks/"에 배경이 제거된 png 이미지 파일을 넣는다. (원본 이미지와 이름이 같아야한다.)
4. python test.py [Dall-E key] 를 입력하여 실행한다. (command argument 생략 시 아웃페인팅 생략)
5. "images/" 혹은 사용자 지정 위치에 새로운 폴더가 만들어져서 확장된 이미지가 저장된다.



# batch mode
샘플 이미지에서 일정 비율 추출하여 한꺼번에 새로운 output 폴더(output_folder_name)에 결과물을 저장한다.

# single mode
test.jpg or test.png를 읽고, test_output.jpg or test_output.png를 출력한다.

# google drive link
https://drive.google.com/drive/folders/1gVvpCkFcvFlD0GDZK4VWygOIb_rqFXem?usp=drive_link


# issue
- 더이상 사용할 것 같지 않은 white_border_adder 파일을 삭제할까요?(11/20)
- 일관성을 위해 paddingProcessor에서 padding_generator로 파일 및 클래스 명 변경하였습니다.(11/20)
- foreground라는 표현은 전경(앞쪽에 보이는 경치)을 뜻하기 때문에 subject(피사체)라는 표현으로 바꾸는 것이 좋지 않을까요?(11/20)

