from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError   #для  сообщ об ошибке login уже занят
from django.contrib.auth import login   #


def signupuser(request):        #страница с запросом имени и паролей
    if request.method == 'GET':         #при вызове через метод 'GET' (через urls.py  или строку в браузере)
        return render (request, 'todo/signupuser.html', {'form':UserCreationForm()}) #отобразится страница с запросом имени и паролей
    else:                   #при вызове через метод 'POST' (нажали кнопку Sign Up на этой странице)
        if request.POST['password1'] == request.POST['password2']: # проверка что пароли равны
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save() #запись учетных данных в dbSql
                login(request, user)     # регистрация пользователя с введенными уч. данными
                return redirect('currenttodos') # редирект на страниу currenttodos


            except IntegrityError:  #исключение для ошибки "логин занят"
                return render (request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please chose a new username!'}) #вывод страницы регистрации с сообщ об ошибке login уже занят
        else:
            return render (request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})  #вывод страницы регистрации с сообщ об ошибке пароли не совпадают

def currenttodos(request):      #отобразится страница с текущими todos
    return render (request, 'todo/currenttodos.html') #отобразится страница с запросом имени и паролей
