from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions, generics
from rest_framework.response import Response
from .serializers import UserAvailableLessonsWithStatsSerializer, UserSerializer, ProductSerializer, LessonSerializer, UserProductAvailableLessonsWithStatsSerializer, ProductStatSerializer
from .models import UserProductLessonHistory, User, Product, Lesson
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import FilteredRelation, Q, F
from django.db.models import Count, Case, When, IntegerField, Value, ExpressionWrapper, BooleanField, Sum

class UserAvailableLessonsWithStats(generics.ListAPIView):
    serializer_class = UserAvailableLessonsWithStatsSerializer
    def get_queryset(self):
        user_name = self.kwargs['user']
        return UserProductLessonHistory.objects.filter(user__name=user_name).annotate(was_watched=ExpressionWrapper(Q(whatch_time__gte=F("lesson__length_in_seconds")*0.8), output_field=BooleanField()))

class UserProductAvailableLessonsWithStats(generics.ListAPIView):
    serializer_class = UserProductAvailableLessonsWithStatsSerializer
    def get_queryset(self):
        user_name = self.kwargs['user']
        product = self.kwargs['product']
        return UserProductLessonHistory.objects.filter(user__name=user_name).filter(product__name=product).annotate(was_watched=ExpressionWrapper(Q(whatch_time__gte=F("lesson__length_in_seconds")*0.8), output_field=BooleanField()))

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
    serializer_class = ProductStatSerializer
    queryset = UserProductLessonHistory.objects.all()
    def get_queryset(self):
        product = self.kwargs['product']
        #whatch_time field
        qs = UserProductLessonHistory.objects.filter(product__name=product).annotate(was_watched=ExpressionWrapper(Q(whatch_time__gte=F("lesson__length_in_seconds")*0.8), output_field=BooleanField()))
        #total_lessons_watched field
        # lessons_wathced = qs.aggregate(wathced_lessons=Count(Case(When(was_watched=True, then=Value(1)))))
        lessons_wathced = -1
        qs = qs.annotate(total_lessons_watched=Value(lessons_wathced))
        #total_watch_time field
        total_watch_time = UserProductLessonHistory.objects.filter(product__name=product).aggregate(Sum('whatch_time'))['whatch_time__sum']
        qs = qs.annotate(total_watch_time=Value(total_watch_time))
        # total_number_students field
        qs = qs.annotate(total_number_students=Value(1))
        # acquering_percent field
        qs = qs.annotate(acquering_percent=Value(1))
        return qs