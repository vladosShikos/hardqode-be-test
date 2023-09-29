from elearning.models import Product, Lesson
from elearning.serializers import *
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch

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
        lessons =   UserLessonHistory.objects.select_related('lesson', 'user', 'product').filter(user__username=user.username)
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
        lessons =   UserLessonHistory.objects.select_related('lesson', 'user', 'product').filter(product__title=product_title, user__username=user.username)
        lessons_json = self.get_serializer(lessons, many=True)
        return Response(lessons_json.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True,
            methods=['get'],    
            url_path='stats', 
            serializer_class=None)
    def get_product_stats(self, request, *args, **kwargs):
        product = self.get_object()
        queryset = UserLessonHistory.objects.filter(product__title=product.title)
        lessons_watched = queryset.filter(was_watched=True).count()
        watch_time_from_all_students = queryset.aggregate(Sum('watch_time'))["watch_time__sum"]
        number_of_students = queryset.values('user').distinct().count()
        acquere_percent = number_of_students / User.objects.count()
        response_body = {'lessons_watched':lessons_watched,
                        'watch_time_from_all_students':watch_time_from_all_students,
                        'number_of_students':number_of_students,
                        'acquere_percent':acquere_percent
                    }
        return Response(response_body)
    
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class ProductAccessViewSet(viewsets.ModelViewSet):
    queryset = ProductAccess.objects.all()
    serializer_class = ProductAccessSerializer

class UserLessonHistoryViewSet(viewsets.ModelViewSet):
    queryset = UserLessonHistory.objects.all()
    serializer_class = UserLessonHistorySerializer

class ProductStatViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        product_lessons = UserLessonHistory.objects.filter(product_id=pk)
        lessons_watched = product_lessons.filter(was_watched=True).count()
        watch_time_from_all_students = product_lessons.aggregate(Sum('watch_time'))["watch_time__sum"]
        number_of_students = product_lessons.values('user').distinct().count()
        acquere_percent = number_of_students / User.objects.count()
        response_body = {'lessons_watched':lessons_watched,
                        'watch_time_from_all_students':watch_time_from_all_students,
                        'number_of_students':number_of_students,
                        'acquere_percent':acquere_percent
                    }
        return Response(response_body)