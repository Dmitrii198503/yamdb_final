from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .pagination import NumberPagination
from .permissions import (
    CommentPermission, IsAdmin, IsAdminOrReadonly, ReviewPermission,
)
from .serializers import (
    AdminSerializer, CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitlesSerializer, TokenSerializer, UserEmailSerializer,
    UserSerializer,
)
from api_yamdb import settings
from reviews.models import Category, Genre, Review, Title
from users.models import User


@api_view(
    ["post"],
)
def signup(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(User, username=request.data.get("username"))
    if not user.confirmation_code:
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()
    send_mail(
        subject="Confirmation code",
        message=f"{user.confirmation_code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=(user.email,),
    )
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(["post"])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data.get("username"))

    if default_token_generator.check_token(
        user, serializer.data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = "username"
    permission_classes = [
        IsAdmin,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ("username",)
    pagination_class = LimitOffsetPagination

    @action(
        methods=["patch", "get"],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path="me",
        url_name="me",
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        if self.request.method == "PATCH" and user.role != "user":
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs["title_id"])
        review = get_object_or_404(
            Review, pk=self.kwargs["review_id"], title=title
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs["title_id"])
        review = get_object_or_404(
            Review, pk=self.kwargs["review_id"], title=title
        )
        author = self.request.user
        serializer.save(author=author, review=review)


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [ReviewPermission]

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs["title_id"])
        review = title.reviews.get(id=self.kwargs["pk"])
        author = self.request.user
        if (
            not self.request.user.is_authenticated
            or self.request.user != review.author
        ):
            raise PermissionDenied("запрещено обновлять")
        serializer.save(author=author, title=title)

    def perform_create(self, serializer):
        title_id = self.kwargs["title_id"]
        title = get_object_or_404(Title, pk=title_id)
        author = self.request.user
        if title.reviews.filter(author=author).exists():
            raise ValidationError("Пост существует")

        serializer.save(author=author, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs["title_id"])
        return title.reviews.all()


class TitleViewSet(viewsets.ModelViewSet):
    """Title view, create and update methods deal
    with genre and cathegory save, also custom
    filter added.
    """

    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAdminOrReadonly,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        slug_genre = self.request.data.get("genre")
        if isinstance(slug_genre, str):
            slug_genre = self.request.data.getlist("genre")
        slug_category = self.request.data.get("category")
        genre = Genre.objects.filter(slug__in=slug_genre)
        category = get_object_or_404(Category, slug=slug_category)
        serializer.save(genre=genre, category=category)

    def perform_update(self, serializer):
        slug_genre = self.request.data.get("genre")
        slug_category = self.request.data.get("category")
        if slug_genre and slug_category:
            genre = Genre.objects.filter(slug__in=slug_genre)
            category = get_object_or_404(Category, slug=slug_category)
            serializer.save(genre=genre, category=category)
        elif slug_genre:
            genre = get_list_or_404(Genre, slug__in=slug_genre)
            serializer.save(genre=genre)
        elif slug_category:
            category = get_object_or_404(Category, slug=slug_category)
            serializer.save(category=category)
        else:
            serializer.save()


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Genre view based on mixins"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = NumberPagination
    lookup_field = "slug"
    permission_classes = [
        IsAdminOrReadonly,
    ]
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Cathegory view based on mixins"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = NumberPagination
    lookup_field = "slug"
    permission_classes = [
        IsAdminOrReadonly,
    ]
    filter_backends = [SearchFilter]
    search_fields = ["name"]
