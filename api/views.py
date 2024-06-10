from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework import permissions, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Album, Quote, User
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    AlbumSerializer,
    AuthenticatedUserSerializer,
    QuoteSerializer,
    UserSerializer,
)

# def logout(request):
#     auth_logout(request)
#     return redirect("/")


# @api_view(["GET"])
# def index(request, format=None):
#     return Response(
#         {
#             "users": reverse("user-list", request=request, format=format),
#             "albums": reverse("album-list", request=request, format=format),
#             "quotes": reverse("quote-list", request=request, format=format),
#         }
#     )


class AlbumViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Album.objects.all().order_by("-date")  # Order by date descending
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuoteViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Quote.objects.all().order_by("-date")  # Order by date descending
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == "get_authenticated_user":
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "get_authenticated_user":
            return AuthenticatedUserSerializer
        return UserSerializer

    @action(detail=False, methods=["get"], url_path="me")
    def get_authenticated_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
