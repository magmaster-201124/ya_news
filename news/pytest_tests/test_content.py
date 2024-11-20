import pytest

from django.urls import reverse
from django.conf import settings

from news.forms import CommentForm
from news.models import News


@pytest.mark.django_db
def test_homepage_count_news(client, list_news_add):
    """Количество новостей на главной странице должно быть не более 10."""
    url = reverse('news:home')
    response = client.get(url)
    list_response = response.context['object_list']
    assert len(list_response) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_homepage_news_sorted(client, list_news_add):
    """Порядок сортировки новостей от самой свежей к самой старой."""
    url = reverse('news:home')
    response = client.get(url)
    list_response = response.context['object_list']
    sorted_news = News.objects.order_by('date')
    sorted_news = list(reversed(sorted_news))
    del sorted_news[-1]
    assert list(list_response) == sorted_news


@pytest.mark.django_db
def test_authorized_client_has_form(user_client, news):
    """Доступность формы комментария для авторизованного клиента."""
    url = reverse('news:detail', args=[news.pk])
    user_response = user_client.get(url)
    assert isinstance(user_response.context['form'], CommentForm)


@pytest.mark.django_db
def test_anonimous_client_has_not_form(client, news):
    """Доступность формы комментария для анонимного клиента."""
    url = reverse('news:detail', args=[news.pk])
    anonimous_response = client.get(url)
    assert 'form' not in anonimous_response.context


@pytest.mark.django_db
def test_comments_order(client, news, comment, comment_2):
    """Комментарии на странице новости отсортированы от старых к новым."""
    url = reverse('news:detail', args=(news.pk,))
    client_response = client.get(url)
    comments = client_response.context['news'].comment_set.all()
    assert comments[0].created < comments[1].created
