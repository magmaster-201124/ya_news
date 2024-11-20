from http import HTTPStatus

import pytest

from django.urls import reverse

from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'target',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonimous_client(client, target):
    """Cтраницы входа, выхода, регистрации и главная доступны всем клиентам."""
    url = reverse(target)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_page_for_anonimous_client(client, news):
    """Страница отдельной новости доступна анонимному пользователю."""
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'target',
    ('news:edit', 'news:delete')
)
def test_pages_availability_for_author_comment(user_client, target, comment):
    """Cтраницы редактирования и удаления комментария доступны автору."""
    url = reverse(target, args=(comment.pk,))
    response = user_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'target',
    ('news:edit', 'news:delete')
)
def test_pages_availability_not_author_comment(user_2_client, target, comment):
    """Cтраницы редактирования и удаления комментария не доступны не автору."""
    url = reverse(target, args=(comment.pk,))
    response = user_2_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    'target',
    ('news:edit', 'news:delete')
)
def test_redirect_anonymous(client, target, comment):
    """Переадресация на логин со страниц редактирования и удаления коммента."""
    login_url = reverse('users:login')
    url = reverse(target, args=(comment.pk,))
    response = client.get(url)
    redirect_url = f'{login_url}?next={url}'
    assertRedirects(response, redirect_url)
