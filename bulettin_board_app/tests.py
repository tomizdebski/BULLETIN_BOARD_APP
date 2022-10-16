from django.test import TestCase
from django.conf import settings
import pytest
from django.urls import reverse
from bulettin_board_app.models import Category, Locations, Announcement, Photos


@pytest.mark.django_db
def test_index_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_view(client):
    url = reverse('add_announce')
    response = client.get(url)
    assert response.status_code == 200

