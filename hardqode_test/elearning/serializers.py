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
    was_watched = serializers.BooleanField()
    class Meta:
        model = UserProductLessonHistory
        fields = ['user', 'product', 'lesson', 'whatch_time', 'was_watched']


class UserProductAvailableLessonsWithStatsSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer
    Products = ProductSerializer    
    lessons = LessonSerializer
    was_watched = serializers.BooleanField()
    class Meta:
        model = UserProductLessonHistory
        fields = ['user', 'product', 'lesson', 'whatch_time', 'was_watched', 'last_watch_date']

class ProductStatSerializer(serializers.HyperlinkedModelSerializer):
    # user = UserSerializer
    # Products = ProductSerializer    
    # lessons = LessonSerializer
    # lessons = LessonSerializer(many=True, read_only=True)
    # was_watched = serializers.BooleanField()
    # Количество просмотренных уроков от всех учеников.
    total_lessons_watched = serializers.IntegerField()
    # Сколько в сумме все ученики потратили времени на просмотр роликов.
    total_watch_time = serializers.IntegerField()
    # Количество учеников занимающихся на продукте.
    total_number_students = serializers.IntegerField()
    # Процент приобретения продукта (рассчитывается исходя из количества полученных доступов к продукту деленное на общее количество пользователей на платформе).
    acquering_percent = serializers.IntegerField()
    class Meta:
        model = UserProductLessonHistory
        # fields = ['user', 'product', 'lessons', 'whatch_time', 'last_watch_date', 'was_watched']
        fields = ['total_lessons_watched', 'total_number_students', 'acquering_percent', 'total_watch_time']