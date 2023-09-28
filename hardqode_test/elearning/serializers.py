from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserLessonHistory, Product, Lesson



class UserSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedIdentityField(many=True, view_name='product-detail', read_only=True)
    class Meta:
        model = User
        fields = ['url','name', 'products']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url','title', 'owner', 'lessons']


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = ['url', 'title', 'lesson_url', 'length_in_seconds']


