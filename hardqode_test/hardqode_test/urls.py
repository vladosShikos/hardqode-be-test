"""
URL configuration for hardqode_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from elearningbe import views

router = routers.DefaultRouter()
# router.register(r'userAvailableLessonsWithStats', views.UserAvailableLessonsWithStatsViewSet)
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'products', views.ProductViewSet)
# router.register(r'products-stats', views.ProductStatsViewSet)
router.register(r'lessons', views.LessonViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('userAvailableLessonsWithStats/<str:user>/', views.UserAvailableLessonsWithStats.as_view()),
    path('userAvailableLessonsWithStats/<str:user>/<str:product>', views.UserProductAvailableLessonsWithStats.as_view()),
    path('products-stats/<str:product>', views.ProductStats.as_view())
]
