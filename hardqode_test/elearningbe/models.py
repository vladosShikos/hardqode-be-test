from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    owners = models.ManyToManyField(User, through="ProductAccessToken")
    lessons = models.ManyToManyField("Lesson")
    def __str__(self):
        return self.name

class ProductAccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_acquired = models.DateTimeField()
    valid_thru = models.DateTimeField()
    def __str__(self):
        return f"{self.user}-{self.product}"

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    length_in_seconds = models.IntegerField(default=0)
    accessable_to = models.ManyToManyField(User, through="UserProductLessonHistory")
    def __str__(self):
        return self.name

class UserProductLessonHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    whatch_time = models.IntegerField(default=0)
    last_watch_date = models.DateTimeField()
    def __str__(self):
        return f"{self.user}-{self.product}-{self.lesson}"

    @property
    def was_watched(self):
        return self.whatch_time >= 0.8* self.lesson.length_in_seconds
    