from rest_framework import serializers
from django.contrib.auth.models import User
from elearning.models import *
from django.db import models
from django.db.models import Sum



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url','username']
    

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url','title', 'owner', 'lessons', 'available_to']


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = ['url', 'title', 'lesson_url', 'length_in_seconds']

class ProductAccessSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer
    product = ProductSerializer
    class Meta:
        model = ProductAccess
        fields = ['url', 'user', 'product', 'date_acquired', 'valid_thru']
    

class UserLessonHistorySerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer
    product = ProductSerializer
    lesson = LessonSerializer
    class Meta:
        model = UserLessonHistory
        fields = ['url','user', 'product', 'lesson', 'watch_time', 'last_watch_date', "was_watched"]


class UserAvailableLessonsSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.title')
    lesson = serializers.ReadOnlyField(source='lesson.title')
    class Meta:
        model = UserLessonHistory
        fields = [ 'product', 'lesson',  "was_watched", 'watch_time', ]

class UserPerProductAvailableLessonsSerializer(UserAvailableLessonsSerializer):
    class Meta:
        model = UserLessonHistory
        fields = [ 'product', 'lesson',  "was_watched", 'watch_time', 'last_watch_date']

class ProductStatsSerializer(serializers.ModelSerializer):
    lessons_watched = serializers.SerializerMethodField('count_watched_lessons')
    watch_time_from_all_students = serializers.SerializerMethodField('sum_watch_time_from_all_students')
    number_of_students = serializers.SerializerMethodField('count_students')
    acquire_percent = serializers.SerializerMethodField('get_acquire_percent')
    class Meta:
        model = Product
        fields = ['lessons_watched', 'watch_time_from_all_students', 'number_of_students', 'acquire_percent']

    def count_watched_lessons(self, product):
        lessons_watched = UserLessonHistory.objects.filter(product__title=product.title, was_watched=True).count()
        return lessons_watched
    
    def sum_watch_time_from_all_students(self, product):
        watch_time_from_all_students = UserLessonHistory.objects.filter(product__title=product.title).aggregate(Sum('watch_time'))
        return watch_time_from_all_students["watch_time__sum"]
    
    def count_students(self, product):
        number_of_students = UserLessonHistory.objects.filter(product__title=product.title).values('user').distinct().count()
        return number_of_students
    
    def get_acquire_percent(self, product):
        acquire_percent = UserLessonHistory.objects.filter(product__title=product.title).values('user').distinct().count() / User.objects.count()
        return acquire_percent


    