from django.db import models
from django.contrib.auth.models import User
import os

# 모델 = 데이터를 저장하는 단위, 웹페이지에서 add-post 클릭하면 나오는 기능들 모음

# 모델 필드를 추가할때마다 migration 해줘야한다.
# (venv) python manage.py makemigrations
# (venv) python manage.py migrate
# blank=True 필수는 아니다, 데이터가 없어도 생성 >> if~ else 구분안해도 문제는 없다. if~ else 필수는 head_image 처럼 case 가 다를때

class Post(models.Model): # Post라는 모델 클래스, 모델 클래스 이름 = Post
    title = models.CharField(max_length=30) # title 모델 필드, 글자수 제한
    hook_text = models.CharField(max_length=100, blank = True) # 블로그 페이지가 돋보이게

    content = models.TextField() # content 모델 필드, 무한대 입력

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank =True) # 이미지 업로드한 날짜를 기준으로 설정
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank =True) # 파일 업로드한 날짜를 기준으로 설정

    created_at = models.DateTimeField(auto_now_add=True) # Date 모델 필드, Time 모델 필드 자동으로 날짜 생성해 추가
    # 새로 작성했을 때 생성 : auto_now_add
    updated_at = models.DateTimeField(auto_now=True) #Model을 생성때마다 migration 해줘
    # 수정했을 때 업데이트 : auto_now


    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


    # self = 자기 자신을 의미함

    def __str__(self): # _str_ 함수로 모델의 string 표현 방법 정의하기, 그냥 {{p}}일 때 출력되는 pk와 title
        return f'[{self.pk}]{self.title} :: {self.author}' # 번호[Primary Key]와 타이틀을 합해 인덱스에 표시


    def get_absolute_url(self): ## 목록페이지와 상세페이지를 연결함
        return f'/blog/{self.pk}' ## get_absolute_rul 함수를 생성하면, admin 사이트에 자동으로 VIEW ON SITE 버튼이 생성, 누르면 상세페이지 이동


    ## 1. 파일 업로드 함수, 이름 가지고옴

    def get_file_name(self):
        return os.path.basename(self.file_upload.name) #os.path에 있는 basename함수 가지고 오기 자기자신의 파일 업로드된 이름을 가지고옴


    ## 2. 파일 업로드 함수, 확장자 가지고옴

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
        # return self.get_file_name().split('/')[-1]

        # 1번 get_file_name 함수를 불러와 파일 이름을 가지고온다, '.'을 기준으로 확장자를 분리해 두개의 문자열을 리턴.
        # [-1]은 배열의 마지막 원소를 의미한다. 따라서 확장자를 리턴한다.

