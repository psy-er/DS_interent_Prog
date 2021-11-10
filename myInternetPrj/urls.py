"""myInternetPrj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

# blog 폴더에 urls.py를 생성해서 include 부분 보내줘야함. App폴더에 urls.py 생성해 놨음
# single_pages 폴더에 urls.py 생성해서 include 부분 보내줘야함.
#따라서 blog/urls를 만들고 거기에 path 새로 생성

urlpatterns = [
    path('blog/', include('blog.urls')), #http://서버IP/blog
    path('admin/', admin.site.urls), #http://서버IP/admin
    path('', include('single_pages.urls')), #http://서버IP/
    path('markdownx/',include('markdownx.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)   #서버IP/media/