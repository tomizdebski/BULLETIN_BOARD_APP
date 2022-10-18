from django.test import TestCase
from django.conf import settings
import pytest
from django.urls import reverse
from bulettin_board_app.conftest import user
from bulettin_board_app.models import Category, Locations, Announcement, Photos


@pytest.mark.django_db
def test_index_view(client):
    """
    Test get index
    :param client:
    :return:
    """
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_add_announce_view(client):
    """
    Test get add announce
    :param client:
    :return:
    """
    url = reverse('add_announce')
    response = client.get(url)
    assert response.status_code == 302
    url_redirect = reverse('index')
    assert response.url.startswith(url_redirect)


@pytest.mark.django_db
def test_post_add_announce_view(client, user, category, locations):
    """
    Test post add announce
    :param client:
    :param user:
    :param category:
    :param locations:
    :return:
    """
    url = reverse('add_announce')
    client.force_login(user)
    data = {
        'name': 'Test',
        'description': 'Test',
        'category': category.id,
        'city': locations.city,
        'street': locations.street,
        'province': locations.province,
        'zipcode': locations.zipcode,
        'country': locations.country
    }
    response = client.post(url, data)
    assert response.status_code == 302
    url_redirect = reverse('index')
    assert response.url.startswith(url_redirect)


@pytest.mark.django_db
def test_my_announce_get_not_login(client):
    """
    Test get my announce not login
    :param client:
    :return:
    """
    url = reverse('my_announce')
    response = client.get(url)
    assert response.status_code == 302
    url_redirect = reverse('users:login')
    assert response.url.startswith(url_redirect)


@pytest.mark.django_db
def test_my_announce_get_login(client, user):
    """
    Test get my announce login
    :param client:
    :return:
    """
    url = reverse('my_announce')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_edit_announce_get_not_login(client):
#     """
#     Test get edit announce not login
#     :param client:
#     :return:
#     """
#     url = reverse('my_announce')
#     response = client.get(url)
#     assert response.status_code == 302
#     url_redirect = reverse('users:login')
#     assert response.url.startswith(url_redirect)



