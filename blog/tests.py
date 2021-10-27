from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_james = User.objects.create_user(username='James', password='somepassword')
        self.user_trump = User.objects.create_user(username='Trump', password='somepassword')

        self.category_programming = Category.object.create(name = 'programming',slug='programming')
        self.category_culture = Category.object.create(name='culture', slug='culture')

        # 포스트(게시물)이 3개 존재하는 경우
        self.post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World!! We are the world...',
            author = self.user_james,
            category = self.category_programming
        )
        self.post_002 = Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = '1등이 전부가 아니잖아요',
            author = self.user_trump,
            category = self.category_culture
        )
        self.post_003 = Post.objects.create(
            title = '세 번째 포스트입니다.',
            content = '세 번째 포스트입니다.',
            author = self.user_trump
        )
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

    def category_test(self,soup):
        category = soup.find('div',id = 'categories-card')
        self.assertIn('Categories',category.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', category.text)
        self.assertIn(f'{self.category_culture.name} ({self.category_culture.post_set.count()})', category.text)
        self.assertIn(f'미분류 (1)', category.text)

    def test_post_list(self):
        self.assertEqual(Post.objects.count(),3)

        # 포스트 목록 페이지를 가져온다
        response = self.client.get('/blog/')
        # 정상적으로 페이지가 로드
        self.assertEqual(response.status_code, 200)  # 상태가 200과 같은가?
        # 페이지 타이틀 'Blog'
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')  # soup 이 받은 분석된 내용의 제목이 'Blog'와 같은가?

        self.navbar_test(soup)
        self.category_test(soup)

        # 포스트(게시물)의 타이틀이 3개 존재하는가
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        main_area = soup.find('div', id='main-area') # 앞에서 받은 soup html 분석 결과에서 <div> 태그에 id가 'main-area'인것을 find 찾는다

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text) # main_area의 텍스트에서 post_001의 제목이 포함되는가?
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text) # main_area의 텍스트에서 post_001의 제목이 포함되는가?
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text) # main_area의 텍스트에서 post_001의 제목이 포함되는가?
        self.assertIn('미분류', post_003_card.text)

        self.assertNotIn('아직 게시물이 없습니다.',main_area.text) # main_area의 텍스트에 '아직~'문장이 포함되는가?
        self.assertIn(self.user_james.username.upper(),main_area.text)
        self.assertIn(self.user_trump.username.upper(), main_area.text)

        # 포스트(게시물)이 하나도 없는 경우에
        Post.objects.all().delete
        self.assertEqual(Post.objects.count(), 0)  # Post 모델 import
        # 포스트 목록 페이지를 가져온다
        response = self.client.get('/blog/')
        # 정상적으로 페이지가 로드
        self.assertEqual(response.status_code, 200)  # 상태가 200과 같은가?
        # 페이지 타이틀 'Blog'
        soup = BeautifulSoup(response.content, 'html.parser')


    def test_post_detail(self): # 디테일 상세페이지에 대한 함수

        # 이 포스트의 url이 /blog/1
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1') # 상세페이지에 대한 주소

        # url에 의해 정상적으로 상세페이지를 불러오는가
        response = self.client.get('/blog/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser') #위에 코드 복붙

        self.navbar_test(soup)
        self.category_test(soup)

        # 포스트의 title은 웹브라우저의 title에 있는가
        self.assertIn(self.post_001.title, soup.title.text)

        # 포스트의 title은 포스트영역에도 있는가
        main_area = soup.find('div', id='main-area') # 위에 코드 복붙
        post_area = main_area.find('div',id = "post-area") # 포스트 영역 추가
        self.assertIn(self.post_001.title, post_area.text) # 위에 코드 복붙
        self.assertIn(self.post_001.category.name, post_area.text) # 위에 코드 복붙
        # 포스트 작성자가 있는가
        # 아직 작성중
        # 포스트의 내용이 있는가
        self.assertIn(self.post_001.content, post_area.text)

        self.assertIn(self.user_james.username.upper(),post_area.text)