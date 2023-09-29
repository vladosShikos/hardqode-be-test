from elearning.models import Product, Lesson
from elearning.serializers import *
from rest_framework import viewsets
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class ProductAccessViewSet(viewsets.ModelViewSet):
    queryset = ProductAccess.objects.all()
    serializer_class = ProductAccessSerializer

class UserLessonHistoryViewSet(viewsets.ModelViewSet):
    queryset = UserLessonHistory.objects.all()
    serializer_class = UserLessonHistorySerializer