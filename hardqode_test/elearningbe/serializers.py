from .models import UserProductLessonHistory, User, Product, Lesson
from rest_framework import serializers



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['name']


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'url', 'length_in_seconds', 'accessable_to']



class ProductSerializer(serializers.HyperlinkedModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = UserProductLessonHistory
        fields = ['name', 'owners', 'lessons']



class UserAvailableLessonsWithStatsSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer
    Products = ProductSerializer    
    lessons = LessonSerializer
    class Meta:
        model = UserProductLessonHistory
        fields = ['user', 'product', 'lesson', 'whatch_time', 'was_watched']


class UserProductAvailableLessonsWithStatsSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer
    Products = ProductSerializer    
    lessons = LessonSerializer
    class Meta:
        model = UserProductLessonHistory
        fields = ['user', 'product', 'lesson', 'whatch_time', 'was_watched', 'last_watch_date']

class ProductStatSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer
    Products = ProductSerializer    
    lessons = LessonSerializer
    lessons = LessonSerializer(many=True, read_only=True)
    was_watched = serializers.BooleanField()
    class Meta:
        model = UserProductLessonHistory
        fields = ['user', 'product', 'lessons', 'whatch_time', 'last_watch_date', 'was_watched']