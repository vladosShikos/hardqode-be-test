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

    