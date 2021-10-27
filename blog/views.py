from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
#views 파일에서 홈페이지에 작성된 Post에 있는 내용을 다 import

# Create your views here.
##-------------------[CBV]--------------------------------
## 매개변수로 ListView, DetailView를 받는다.
## ListView는 (모델명)_list.html을 자동으로 템플릿이라고 인지한다. 따라서 별도로 경로를 적을 필요가 없다.
## DetailView는 (모델명)_detail.html을 자동으로 템플릿이라고 인지한다. 따라서 별도로 경로를 적을 필요가 없다.

class PostList(ListView) : #PostList(모델이름+List) 클래스 추가, 매개변수 ListView import
    model = Post #모델추가
    ordering = '-pk'

#    [1.명시적으로 웹사이트 불러오기] 디폴트 X 내가 지정한 템플릿을 부를때, 웹사이트 불러오기
#    template_name = 'blog/post_list.html'
#    연결되는 템플릿의 이름 = post_list.html , 연결됨 따라서
#    DS_internet_Prog/blog/templates/blog/index 불필요
##    > index을 post_list로, single_post_pages를 post_detail로 변경하면 자동적으로 템플릿로 인지한다.
##    이름 변경시 Refator > Rename > DoRefator
#    [2.자동으로 웹사이트 불러오기]


class PostDetail(DetailView) : #PostDetail(모델이름+Detail) 클래스 추가, 매개변수 DetailView import
    model = Post #모델추가

#    연결되는 템플릿의 이름 = post_detail.html, 연결됨됨

# -------------------[FBV]---------index.html 삭제됨----------------------
## blog/urls에서 호출한 view파일의 index 함수
## blog/index.html은 요청된 템플릿(html)이다. 즉 보여질 html이다.
## render : 화면에 보여지는 과정을 만드는 함수
## blog/index.html = blog/templates/blog/index.html

## (생성) blog앱에 templates 폴더생성 > blog 폴더생성 > index.html 문서 파일 생성


#def index(request) :
#    // posts = Post.objects.all().order_by('-pk') # 작성된 글의 데이터베이스에 있는 objects(레코드) 모두를 역순으로 가지고 와라
#    // render = 화면에 보이는 구성을 정의 render(request, 템플릿)
#    return render (request, 'blog/post_list.html', #FBV에서는 클래스가 없어서 받을 주소경로를 적어줘야한다.
#                  {
#                       'posts' : //posts  ## 홈페이지에서 작성된 posts에 저장된 내용을 index.html의의 'posts'에 옮겨라
#                   }
#                   )
#
#def single_post_page(request, pk) : ## 포스트 primarykey 전달
#    post = Post.objects.get(pk=pk)  ## 모든 데이터베이스 .all() 대신 특정 정보 불러옴 .get()
#                                    ## pk=pk 왼쪽 pk는 모델의 필드이름, 오른쪽은 매개변수 pk로 필드에 넣어줌
#    return render (request, 'blog/post_detail.html',
#                   {
#                       'post' : post
#                   }
#                   )
