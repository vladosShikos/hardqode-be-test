from django.db import models

class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE, default='') #type:ignore
    accessable_to = models.ForeignKey('ProductAccessToken', on_delete=models.CASCADE)
    lessons = models.ManyToManyField("Lesson")

class ProductAccessToken(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_acquired = models.DateTimeField()
    valid_thru = models.DateTimeField()

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    lesson_url = models.CharField(max_length=200)
    length_in_seconds = models.IntegerField(default=0)

class UserLessonHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watch_time = models.IntegerField(default=0)
    last_watch_date = models.DateTimeField(auto_now_add=True)
    was_watched = models.BooleanField(default=False)

    class Meta:
        ordering = ['user', 'product', 'lesson']

    def save(self, *args, **kwargs):
        self.was_watched = self.watch_time >= 0.8 * self.lesson.length_in_seconds
        super().save(*args, **kwargs)