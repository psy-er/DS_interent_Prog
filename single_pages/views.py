from django.shortcuts import render
from blog.models import Post
# Create your views here.
## render 함수 호출해 웹페이지를 template함.
## single_pages > templates 폴더 만들기 > single_pages 폴더 만들기 > landing.html, about_me.html 파일만들기

def langing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html',
                  {'recent_posts' : recent_posts})


def about_me(request):
    return render(request, 'single_pages/about_me.html')
