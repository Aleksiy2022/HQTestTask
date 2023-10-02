from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """
    Модель продукта.
    """

    title = models.CharField(max_length=250, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    users = models.ManyToManyField(User, related_name='accessible_products', db_index=True, blank=True)

    def __str__(self):
        return self.title

    def get_total_view_time(self):
        total_seconds = sum(lesson.view_time for lesson in self.product.all())
        hours = total_seconds // 3600
        minutes = total_seconds // 60 % 60
        seconds = total_seconds % 60
        return f"{hours} час(ов) {minutes} минут(а) {seconds} секунд(а)"

    def get_total_viewed_lesson(self):
        total_viewed_lesson = sum(lesson.view_status for lesson in self.product.all() if lesson.view_status)
        return total_viewed_lesson


class Lesson(models.Model):
    """
    Модель урока.
    :param duration: продолжительность видеоурока в секундах
    """

    title = models.CharField(max_length=250)
    products = models.ManyToManyField(Product, related_name='lessons', db_index=True, blank=True)
    video_link = models.URLField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class LessonView(models.Model):
    """
    Модель для фиксации данных просмотра урока пользователем.
    :param view_time: значение просмотра фиксируется в секундах
    """

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='viewed_lessons')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    view_time = models.PositiveIntegerField()
    view_status = models.BooleanField(default='False')
    last_viewing = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        time_threshold = self.lesson.duration * 0.8
        if self.view_time >= time_threshold:
            self.view_status = True
        super().save(*args, **kwargs)
