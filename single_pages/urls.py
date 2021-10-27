from django.urls import path
from . import views

urlpatterns = [ # 서버IP/
    path('', views.langing), # 서버IP/ 대문페이지, views의 langing 함수 호출.
    path('about_me/',views.about_me) # 서버IP/about_me/ ,views의 about_me 함수 호출.
]