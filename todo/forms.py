from django.forms import ModelForm
from .models import Todo  # импортируем класс Todo из models.py

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']     # это те поля из models.py класса Todo, которые нам нужно заполнять.
