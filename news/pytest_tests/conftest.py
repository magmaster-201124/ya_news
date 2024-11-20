from datetime import datetime, timedelta

import time

import pytest

from django.conf import settings
from django.test.client import Client

from news.models import News, Comment


@pytest.fixture
def user(django_user_model):
    """Авторизованный пользователь."""
    return django_user_model.objects.create(username='User')


@pytest.fixture
def user_2(django_user_model):
    """Авторизованный пользователь 2."""
    return django_user_model.objects.create(username='User_2')


@pytest.fixture
def user_client(user):
    """Логин авторизованного пользователя."""
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def user_2_client(user_2):
    """Логин авторизованного пользователя 2."""
    client = Client()
    client.force_login(user_2)
    return client


@pytest.fixture
def news():
    """Тестовая новость."""
    news = News.objects.create(
        title='News_1',
        text='First_news'
    )
    return news


@pytest.fixture
def comment(news, user):
    """Тестовый комментарий."""
    comment = Comment.objects.create(
        news=news,
        author=user,
        text='Comment_1'
    )
    time.sleep(0.01)
    return comment


@pytest.fixture
def comment_2(news, user_2):
    """Тестовый комментарий 2."""
    comment_2 = Comment.objects.create(
        news=news,
        author=user_2,
        text='Comment_2'
    )
    return comment_2


@pytest.fixture
def list_news_add():
    """Список новостей."""
    list_news_add = News.objects.bulk_create(
        News(title=f'News {index}',
             text=f'Simple text {index}.', date=datetime.today() - timedelta(
                 index)) for index in range(
                     settings.NEWS_COUNT_ON_HOME_PAGE + 1))
    return list_news_add


@pytest.fixture
def comment_edit():
    """Текст комментария."""
    return {'text': 'Comment_1_edit'}
