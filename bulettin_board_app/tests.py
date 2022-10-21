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
def test_by_category_view(client, category):
    """
    Test get category view
    :param client:
    :param category:
    :return:
    """
    url = reverse('by_category_view', args=(category.id,))
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
def test_detail_announce_id_view(client, announce):
    """
    Test detail announce
    :param client:
    :param announce.id:
    :return:
    """
    url = reverse('details_announce', args=(announce.id,))
    response = client.get(url)
    assert response.status_code == 200


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


@pytest.mark.django_db
def test_send_email_get_not_login(client, announce):
    """
    Test sending email not login
    :param client:
    :param announce:
    :return:
    """
    url = reverse('send_email', args=(announce.id,))
    response = client.get(url)
    assert response.status_code == 302
    url_redirect = reverse('users:login')
    assert response.url.startswith(url_redirect)


@pytest.mark.django_db
def test_send_email_get_login(client, announce, user):
    """
    Test sending email , query for an annoucement
    :param client:
    :param announce.id :
    :return:
    """
    url = reverse('send_email', args=(announce.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_edit_announce_login_view(client, user, announce):
    """
    Test get edit announce
    :param client:
    :return:
    """
    url = reverse('edit', args=(announce.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_edit_announce_view(client, user, announce, category, locations, photo):
    """
    Test post edit announce
    :param client:
    :return:
    """
    url = reverse('edit', args=(announce.id,))
    client.force_login(user)
    data = {
        'name': 'Test',
        'description': 'Test-desc',
        'category': category.id,
        'city': locations.city,
        'street': locations.street,
        'province': locations.province,
        'zipcode': locations.zipcode,
        'country': locations.country,
        'image1': 'images/test.jpg'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('details_announce', args=(announce.id,))
    #del data['category', 'street', 'province', 'zipcode', 'country', 'image1']
    #Announcement.objects.get(**data)


@pytest.mark.django_db
def test_searching_get_view(client):
    """
    Test get searching
    :param client:
    :return:
    """
    url = reverse('searching')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_searching_post_view(client, announce):
    """
    Test post searching
    :param client:
    :param announce:
    :return:
    """
    url = reverse('searching')
    data = {
        'search': 'Test',
    }
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_delete_announce_login(client, announce, user):
    url = reverse('delete', args=(announce.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_delete_announce_login(client, announce, user):
    url = reverse('delete', args=(announce.id,))
    client.force_login(user)
    response = client.post(url)
    assert response.status_code == 302
    url_redirect = reverse('index')
    assert response.url.startswith(url_redirect)


















