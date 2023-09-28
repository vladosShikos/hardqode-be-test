from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)
    available_to = models.ManyToManyField('auth.User', through='ProductAccess')
    lessons = models.ManyToManyField("Lesson", through='UserLessonHistory')

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    lesson_url = models.CharField(max_length=200)
    length_in_seconds = models.IntegerField(default=0)

class ProductAccess(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date_acquired = models.DateTimeField()
    valid_thru = models.DateTimeField()

class UserLessonHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    watch_time = models.IntegerField(default=0)
    last_watch_date = models.DateTimeField(auto_now_add=True)
    was_watched = models.BooleanField(default=False)

    class Meta:
        ordering = ['user']

    def save(self, *args, **kwargs):
        self.was_watched = self.watch_time >= 0.8 * self.lesson.length_in_seconds
        super().save(*args, **kwargs)