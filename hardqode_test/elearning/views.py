from elearning.models import Product, Lesson
from elearning.serializers import *
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True,
            methods=['get'],
            url_path='available_lessons', 
            url_name='list-available-lessons', 
            serializer_class=UserAvailableLessonsSerializer)
    def list_available_lessons(self, request, *args, **kwargs):
        user = self.get_object()
        lessons =   UserLessonHistory.objects.filter(user__username=user.username)
        lessons_json = self.get_serializer(lessons, many=True)
        return Response(lessons_json.data)
    
    @action(detail=True,
        methods=['get'],
        url_path='available_lessons/(?P<product_title>[^/.]+)', 
        url_name='list-available-lessons', 
        serializer_class=UserPerProductAvailableLessonsSerializer)
    def limit_products(self, request, pk, *args, **kwargs):
        product_title = self.kwargs.get('product_title')
        user = self.get_object()
        print(product_title)
        lessons =   UserLessonHistory.objects.filter(product__title=product_title, user__username=user.username)
        lessons_json = self.get_serializer(lessons, many=True)
        return Response(lessons_json.data)


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

class UserStatsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserStatsSerializer

class PerProductStatViewSet(viewsets.ModelViewSet):
    queryset = UserLessonHistory.objects.all()
    serializer_class = UserLessonHistorySerializer