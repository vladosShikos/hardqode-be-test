from django.urls import path, include
from rest_framework.routers import DefaultRouter
from elearning import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('lessons', views.LessonViewSet, basename='lesson')
router.register('products', views.ProductViewSet, basename='product')
router.register('productsaccesses', views.ProductAccessViewSet, basename='productaccess')
router.register('userlessonhistories', views.UserLessonHistoryViewSet, basename='userlessonhistory')

urlpatterns = [
    path('', include(router.urls)),
]