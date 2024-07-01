from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Album, User
from api.serializers import AlbumSerializer
from unittest.mock import patch

class AlbumModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpass", date_of_birth="1990-01-01"
        )

    def test_album_creation(self):
        album = Album.objects.create(title="Test Album", owner=self.user)
        self.assertEqual(album.title, "Test Album")
        self.assertEqual(album.owner, self.user)


class AlbumSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpass", date_of_birth="1990-01-01"
        )
        self.album = Album.objects.create(title="Test Album", owner=self.user)

    def test_album_serializer(self):
        serializer = AlbumSerializer(self.album)
        data = serializer.data
        self.assertEqual(data["title"], "Test Album")
        self.assertEqual(data["owner"], self.user.email)


class AlbumViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpass", date_of_birth="1990-01-01"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_albums(self):
        Album.objects.create(
            title="Album 1",
            description="Desc 1",
            link_url="http://test1.com",
            thumbnail_url="http://test1.com/thumbnail.jpg",
            date="2024-05-29",
            owner=self.user,
        )
        Album.objects.create(
            title="Album 2",
            description="Desc 2",
            link_url="http://test2.com",
            thumbnail_url="http://test2.com/thumbnail.jpg",
            date="2024-05-28",
            owner=self.user,
        )
        url = reverse("album-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], "Album 1")

    @patch('api.views.send_slack_message')
    def test_create_album(self, mock_send_slack_message):
        mock_send_slack_message.return_value = None  # Mock the Slack function to do nothing

        url = reverse("album-list")
        data = {
            "title": "New Album",
            "description": "New Description",
            "link_url": "http://new.com",
            "thumbnail_url": "http://new.com/thumbnail.jpg",
            "date": "2024-05-29",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 1)
        self.assertEqual(Album.objects.get(id=response.data["id"]).owner, self.user)

    def test_create_album_missing_fields(self):
        url = reverse("album-list")
        data = {"title": "New Album"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_permission_denied_for_unauthenticated_user(self):
        self.client.logout()
        url = reverse("album-list")
        data = {
            "title": "New Album",
            "description": "New Description",
            "link_url": "http://new.com",
            "thumbnail_url": "http://new.com/thumbnail.jpg",
            "date": "2024-05-29",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AlbumPermissionTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="testuser@test.com", password="testpass", date_of_birth="1990-01-01"
        )
        self.user2 = User.objects.create_user(
            email="seconduser@test.com", password="testpass", date_of_birth="1990-02-02"
        )
        self.album = Album.objects.create(title="Test Album", owner=self.user1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_permission_denied_for_other_user(self):
        self.client.logout()
        self.client.force_authenticate(user=self.user2)
        url = reverse("album-detail", args=[self.album.id])
        response = self.client.put(url, {"title": "Updated Album"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)