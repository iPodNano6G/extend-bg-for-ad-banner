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

## 미구현 사항

1. DallE 확장 시 객체 탐지하여 걸러내는 기능 서비스에 적용
    - 테스트와 class로만 구현
2. DallE 상하 확장 미검증
    - 특히, 경계 인접 판단의 경우 좌우 판단만 적용





