from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()

router.register('user', views.UserViewSet, basename="user")
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('block', views.ContentBlockViewSet, basename='block')
router.register('img', views.BlockImageViewSet, basename='img')

urlpatterns = [
    # JWT AUTH
    path("obtain-token/", obtain_jwt_token, name="token-auth"),
]

urlpatterns += router.urls