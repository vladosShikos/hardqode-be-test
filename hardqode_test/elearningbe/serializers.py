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
        model = Product
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