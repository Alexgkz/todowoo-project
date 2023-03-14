from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError   #для  сообщ об ошибке login уже занят
from django.contrib.auth import login, logout, authenticate   #
from .forms import TodoForm  # импорт формы страницы создания записей из файла todo/forms.py
from .models import Todo  # импорт модели Todo из файла todo/models.py

def home(request):
    return render (request, 'todo/home.html')

def loginuser(request):
    if request.method == 'GET':         #при вызове через метод 'GET' (через urls.py  или строку в браузере)
        return render (request, 'todo/loginuser.html', {'form':AuthenticationForm()}) #отобразится страница с запросом имени и пароля
    else:                   #при вызове через метод 'POST' (нажали кнопку login )
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])      # проверка есть ли пара login/password и передача их в user
        if user is None:                #если логин пароль неверны повторн загрузка формы с выводом ошибки
          return render (request, 'todo/loginuser.html', {'form':AuthenticationForm(), "error":'Username and password did not match'})
        else:
            login(request, user)     # login пользователя с введенными уч. данными
            return redirect('currenttodos') # редирект на страницу currenttodos

def signupuser(request):        #страница с запросом имени и паролей
    if request.method == 'GET':         #при вызове через метод 'GET' (через urls.py  или строку в браузере)
        return render (request, 'todo/signupuser.html', {'form':UserCreationForm()}) #отобразится страница с запросом имени и паролей
    else:                   #при вызове через метод 'POST' (нажали кнопку Sign Up на этой странице)
        if request.POST['password1'] == request.POST['password2']: # проверка что пароли равны
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save() #запись учетных данных в dbSql
                login(request, user)     # регистрация пользователя с введенными уч. данными
                return redirect('currenttodos') # редирект на страницу currenttodos


            except IntegrityError:  #исключение для ошибки "логин занят"
                return render (request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please chose a new username!'}) #вывод страницы регистрации с сообщ об ошибке login уже занят
        else:
            return render (request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})  #вывод страницы регистрации с сообщ об ошибке пароли не совпадают

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def createtodo(request):
    if request.method == 'GET':         #при вызове через метод 'GET' (через urls.py  или строку в браузере)
        return render (request, 'todo/createtodo.html', {'form':TodoForm()}) #отобразится страница с формой TodoForm() описанной в файле todo/forms.py
    else:   #по нажатию кнопки Create
        try:
            form = TodoForm(request.POST) #все заполнные данные в форме TodoForm
            newtodo = form.save(commit=False)   # записываются в dbDjango
            newtodo.user = request.user     # выполняется привязка данных к пользователю
            newtodo.save()  # и тоже записываются в dbDjango
            return redirect('currenttodos') # редирект на страницу currenttodos
        except ValueError:  # если возникла ошибка неправильных данных ValueError
            return render (request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again'})



def currenttodos(request):          #отобразится страница с текущими todos
        todos = Todo.objects.filter(user=request.user, datacompleted__isnull=True)      #передаются  данные объектов модели Todo для текущего юзера (user=request.user)@ исключения вывода законченных todo(datacompleted__isnull=True)
        return render (request, 'todo/currenttodos.html', {'todos':todos}) #отобразится страница currenttodos.html и ей передаются  данные объектов модели Todo для текущего юзера
