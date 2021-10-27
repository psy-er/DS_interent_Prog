from django.db import models
from django.contrib.auth.models import User
import os

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200,unique=True,allow_unicode=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank = True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank =True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank =True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)



    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, null=True, blank=True , on_delete=models.SET_NULL)



    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'


    def get_absolute_url(self):
        return f'/blog/{self.pk}'




    def get_file_name(self):
        return os.path.basename(self.file_upload.name)


    ## 2. 파일 업로드 함수, 확장자 가지고옴

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
        # return self.get_file_name().split('/')[-1]

        # 1번 get_file_name 함수를 불러와 파일 이름을 가지고온다, '.'을 기준으로 확장자를 분리해 두개의 문자열을 리턴.
        # [-1]은 배열의 마지막 원소를 의미한다. 따라서 확장자를 리턴한다.

