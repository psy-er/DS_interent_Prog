from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_james = User.objects.create_user(username='James', passwd='somepassword')
        self.user_trump = User.objects.create_user(username='Trump', passwd='somepassword')

    def navbar_test(self, soup):
        # 네비게이션바가 있다
        navbar = soup.nav

        # 네비게이션바에 Blog, AboutMe 라는 문구가 있다
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo = navbar.find('a', text='Internet Programming')
        self.assertEqual(logo.atrrs['href'], '/')

        home = navbar.find('a', text='Home')
        self.assertEqual(home.atrrs['href'], '/')

        blog = navbar.find('a', text='Blog')
        self.assertEqual(blog.atrrs['href'], '/blog/')

        about = navbar.find('a', text='About Me')
        self.assertEqual(about.atrrs['href'], '/about_me/')

    def test_post_list(self):
        # 포스트 목록 페이지를 가져온다 // response 변수에 self.client.get('url') 특정 url을 넣어 페이지를 가지고 온다.
        response = self.client.get('/blog/')

        # 정상적으로 페이지가 로드 // status_code 활용해 정상적으로 로드되었는지 확인한다. 200 = OK, 400 = Bad Request, 404 Not Found = 요청한 페이지가 없다
        self.assertEqual(response.status_code, 200)  # 상태가 200과 같은가?

        # 페이지 타이틀 'Blog' // html 을 분석한다 = parser, 분석된 결과를 soup 변수로 받겠다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')  # soup 이 받은 분석된 내용의 제목이 'Blog'와 같은가?

        self.navbar_test(soup)

        # 포스트(게시물)이 하나도 없는 경우에
        self.assertEqual(Post.objects.count(), 0)  # Post 모델 import

        # 적절한 안내 문구가 포함되어 있는지 // id = 'main-area'를 출력하는 부분에 추가한다.
        main_area = soup.find('div', id='main-area')  # 앞에서 받은 soup html 분석 결과에서 <div> 태그에 id가 'main-area'인것을 find 찾는다
        self.assertIn('아직 게시물이 없습니다.', main_area.text)  # 찾은 <div>태그의 text에 '아직~'문장이 포함되는가?

        post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World!! We are the world...',
            author = self.user_james
        )
        post_002 = Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = '1등이 전부가 아니잖아요',
            author = self.user_trump
        )
        self.assertEqual(Post.objects.count(),2) # post의 갯수가 2개인가?

        # 목록페이지를 새롭게 불러와서 //새로 생성했기 때문에 목록페이지를 다시 불러온다.
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser') # 위에 코드 복붙

        # 포스트(게시물)의 타이틀이 2개 존재하는가
        main_area = soup.find('div', id='main-area') # 앞에서 받은 soup html 분석 결과에서 <div> 태그에 id가 'main-area'인것을 find 찾는다
        self.assertIn(post_001.title, main_area.text) # main_area의 텍스트에서 post_001의 제목이 포함되는가?
        self.assertIn(post_002.title, main_area.text) # main_area의 텍스트에서 post_002의 제목이 포함되는가?

        self.assertNotIn('아직 게시물이 없습니다.',main_area.text) # main_area의 텍스트에 '아직~'문장이 포함되는가?
        self.assertIn(self.user_james.username.upper(),main_area.text)
        self.assertIn(self.user_trump.username.upper(), main_area.text)

    def test_post_detail(self): # 디테일 상세페이지에 대한 함수
        # 포스트 하나 생성
        post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World!! We are the world...',
            author = self.user_james

        )

        # 이 포스트의 url이 /blog/1
        self.assertEqual(post_001.get_absolute_url(), '/blog/1') # 상세페이지에 대한 주소

        # url에 의해 정상적으로 상세페이지를 불러오는가
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser') #위에 코드 복붙

        self.navbar_test(soup)

        # 포스트의 title은 웹브라우저의 title에 있는가
        self.assertIn(post_001.title, soup.title.text)

        # 포스트의 title은 포스트영역에도 있는가
        main_area = soup.find('div', id='main-area') # 위에 코드 복붙
        post_area = main_area.find('div',id = "post-area") # 포스트 영역 추가
        self.assertIn(post_001.title, post_area.text) # 위에 코드 복붙

        # 포스트 작성자가 있는가
        # 아직 작성중

        # 포스트의 내용이 있는가
        self.assertIn(post_001.content, post_area.text)

        self.assertIn(self.user_james.username.upper(),post_area.text)