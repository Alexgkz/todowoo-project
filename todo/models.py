from django.db import models
from django.contrib.auth.models import User #для внесения в модель ID пользователя-создателя

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True) # blank=True - МОЖЕТ быть пустым
    created = models.DateTimeField(auto_now_add=True) #auto_now_add=True -автозаполнение текущим временем
    datacompleted = models.DateTimeField(null=True, blank=True) # null=True - МОЖЕТ быть пустым
    important = models.BooleanField(default=False) #чекбокс
    user = models.ForeignKey(User, on_delete=models.CASCADE) #внесение в модель ID пользователя-создателя

    def __str__(self):  #это нужно для отображения имени todo вместо его номера в админке в перечне todo
        return self.title

    # image = models.ImageField(upload_to='portfolio/images/')
    # url = models.URLField(blank=True)
