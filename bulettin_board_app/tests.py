from django.test import TestCase
from django.conf import settings
import pytest
from django.urls import reverse
from bulettin_board_app.models import Category, Locations, Announcement, Photos

# test-get-index
@pytest.mark.django_db
def test_index_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

# test-get-add-announce
@pytest.mark.django_db
def test_add_announce_view(client):
    url = reverse('add_announce')
    response = client.get(url)
    assert response.status_code == 302
    url_redirect = reverse('index')
    assert response.url.startswith(url_redirect)

# test-get-my-announce-not-login
@pytest.mark.django_db
def test_my_announce_get_not_login(client):
    url = reverse('my_announce')
    response = client.get(url)
    assert response.status_code == 302
    url_redirect = reverse('users:login')
    assert response.url.startswith(url_redirect)





