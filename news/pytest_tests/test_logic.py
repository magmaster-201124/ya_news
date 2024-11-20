import pytest

from django.urls import reverse

from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING

from news.models import Comment


@pytest.mark.django_db
def test_comment_anonymous_user(client, news):
    """Невозможность отправки комментария анонимным пользователем."""
    url = reverse('news:detail', args=[news.pk])
    count_befor_post = Comment.objects.count()
    client.post(url, {'text': 'Comment_15'})
    count_after_post = Comment.objects.count()
    assert count_befor_post == count_after_post

@pytest.mark.django_db
def test_comment_authorized_user(user, user_client, news):
    """Возможность отправки комментария авторизованным пользователем."""
    url = reverse('news:detail', args=[news.pk])
    count_befor_post = Comment.objects.count()
    user_client.post(url, {'text': 'Comment_15'})
    count_after_post = Comment.objects.count()
    assert count_befor_post < count_after_post
    comment_test = Comment.objects.get()
    assert comment_test.text == 'Comment_15'
    assert comment_test.news == news
    assert comment_test.author == user


@pytest.mark.django_db
def test_user_cant_use_bad_words(user_client, news):
    """Запрещённые слова в комментарии ведут к неопубликованию его и ошибке."""
    bad_text = {'text': f'Плохие слова: {BAD_WORDS}, ну очень плохие'}
    url = reverse('news:detail', args=(news.pk,))
    count_befor_post = Comment.objects.count()
    error_response = user_client.post(url, bad_text)
    assertFormError(
        error_response,
        form='form',
        field='text',
        errors=WARNING
    )
    count_after_post = Comment.objects.count()
    assert count_befor_post == count_after_post


def test_author_delete_his_comment(user_client, comment):
    """Авторизованный пользователь может удалять свои комментарии."""
    url_for_delete = reverse('news:delete', args=(comment.pk,))
    count_befor_post = Comment.objects.count()
    user_client.post(url_for_delete)
    count_after_post = Comment.objects.count()
    assert count_befor_post > count_after_post


def test_user_cant_delete_other_comment(user_client, comment_2):
    """Авторизованный пользователь не может удалить чужой комментарий."""
    url_for_delete = reverse('news:delete', args=(comment_2.pk,))
    count_befor_post = Comment.objects.count()
    user_client.post(url_for_delete)
    count_after_post = Comment.objects.count()
    assert count_befor_post == count_after_post


def test_author_can_edit_his_comment(user_client, comment_edit, comment):
    """Авторизованный пользователь может редактировать свои комментарии."""
    comment_url = reverse('news:edit', args=(comment.pk,))
    user_client.post(comment_url, comment_edit)
    comment.refresh_from_db()
    assert comment.text == comment_edit['text']


def test_user_cant_edit_other_comment(user_client, comment_edit, comment_2):
    """Авторизованный пользователь не может редактировать чужой комментарий."""
    comment_url = reverse('news:edit', args=(comment_2.pk,))
    user_client.post(comment_url, comment_edit)
    comment_2.refresh_from_db()
    assert comment_2.text != comment_edit['text']
