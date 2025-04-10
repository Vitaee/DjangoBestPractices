import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Magaza
from django.contrib.gis.geos import Point

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='password123'
    )

@pytest.fixture
def magaza(user):
    return Magaza.objects.create(
        ad="Test Store",
        enlem=41.0082,
        boylam=28.9784,
        location=Point(28.9784, 41.0082),
        owner=user
    )

@pytest.mark.django_db
def test_create_magaza(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('magaza-list')
    data = {
        'ad': 'New Test Store',
        'enlem': 41.0082,
        'boylam': 28.9784,
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Magaza.objects.count() == 1
    assert Magaza.objects.get().ad == 'New Test Store'
    assert Magaza.objects.get().owner == user

@pytest.mark.django_db
def test_get_magaza_list(api_client, user, magaza):
    api_client.force_authenticate(user=user)
    url = reverse('magaza-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['ad'] == magaza.ad

@pytest.mark.django_db
def test_update_own_magaza(api_client, user, magaza):
    api_client.force_authenticate(user=user)
    url = reverse('magaza-detail', kwargs={'pk': magaza.pk})
    data = {'ad': 'Updated Store Name'}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    magaza.refresh_from_db()
    assert magaza.ad == 'Updated Store Name'

@pytest.mark.django_db
def test_cannot_update_others_magaza(api_client, magaza):
    other_user = User.objects.create_user(
        username='otheruser',
        email='other@example.com',
        password='password123'
    )
    api_client.force_authenticate(user=other_user)
    url = reverse('magaza-detail', kwargs={'pk': magaza.pk})
    data = {'ad': 'Hacked Store Name'}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    magaza.refresh_from_db()
    assert magaza.ad == 'Test Store'  # unchanged
