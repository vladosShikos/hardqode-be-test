from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions, generics
from rest_framework.response import Response
from .serializers import UserAvailableLessonsWithStatsSerializer, UserSerializer, ProductSerializer, LessonSerializer, UserProductAvailableLessonsWithStatsSerializer
from .models import UserProductLessonHistory, User, Product, Lesson
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import FilteredRelation, Q
from django.db.models import Count, Case, When, IntegerField

class UserAvailableLessonsWithStats(generics.ListAPIView):
    serializer_class = UserAvailableLessonsWithStatsSerializer
    def get_queryset(self):
        user_name = self.kwargs['user']
        return UserProductLessonHistory.objects.filter(user__name=user_name)

class UserProductAvailableLessonsWithStats(generics.ListAPIView):
    serializer_class = UserProductAvailableLessonsWithStatsSerializer
    def get_queryset(self):
        user_name = self.kwargs['user']
        product = self.kwargs['product']
        return UserProductLessonHistory.objects.filter(user__name=user_name).filter(product__name=product)

# class UserAvailableLessonsWithStatsViewSet(viewsets.ModelViewSet):
#     queryset = UserProductLessonHistory.objects.all()
#     serializer_class = UserAvailableLessonsWithStatsSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
  
class ProductStats(generics.ListAPIView):
    serializer_class = UserProductAvailableLessonsWithStatsSerializer
    def get_queryset(self):
        product = self.kwargs['product']
        data = UserProductLessonHistory.objects.filter(product__name=product).annotate(was_watched=Count(Case(When(watch_time__gt=1, then=1),output_field=IntegerField())))
        print(data)
        return data