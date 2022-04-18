from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
    UserViewSet, signup, token,
)

router_v1 = DefaultRouter()
router_v1.register(r"users", UserViewSet)
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(r"genres", GenreViewSet, basename="genres")
router_v1.register(r"categories", CategoryViewSet, basename="categories")
router_v1.register(
    r"titles/(?P<title_id>[^/.]+)/reviews", ReviewViewSet, basename="review"
)

router_v1.register(
    r"titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments",
    CommentViewSet,
    basename="Comment",
)
auth_patterns = [
    path("signup/", signup, name="get_confirmation_code"),
    path("token/", token, name="get_jwt_token"),
]

urlpatterns = [
    path("v1/auth/", include(auth_patterns)),
    path("v1/", include(router_v1.urls)),
]
