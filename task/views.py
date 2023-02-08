from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError ##errores en base de datos
from django.contrib.auth import login,logout, authenticate  ##crea cokies de usuarios
from .forms import TaskForm # importa formulario de crear tarea
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required##proteccion de acceso de rutas

# Create your views here.
# procesa las vistas


def home(request):
    return render(request, 'home.html')

# validacion de datos de usuario


def signup(request):
    # renderiza formulario de acceso de datos
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        # coincidir contraseñas
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()## guarda usuario en la base de datos
                login(request, user)##crea la sesion con cookies
                return redirect('task')#redicecciona pagina
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exist'})



        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'})
##login Usuario
def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html', {
        'form' : AuthenticationForm
    })
    else:
        user = authenticate(request, username = request.POST['username'],
        password = request.POST['password'])

        if user is None:
            return render(request,'signin.html', {
            'form' : AuthenticationForm,
            'error' : 'username or password are incorrect '
            })
        else:
            login(request, user)##crea la sesion con cookies
            return redirect('task')
    
@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def task(request):##filtra las tareas no completadas del usaurio
    task = Task.objects.filter(user =request.user, datecompleted__isnull = True) ## retorna todas las tareas de las bases de datos
    return render(request, 'task.html',{
         'task' : task
    })

@login_required
def task_completed(request):###muestra las tareas completadas
    task = Task.objects.filter(user =request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render(request, 'task.html',{
         'task' : task
    })
@login_required
def task_detail(request,task_id):

    ##task = Task.objects.get(pk=task_id) opcion 1

    if request.method == 'GET':
        task =get_object_or_404(Task,pk=task_id,user=request.user)##Evita caida del servidor
        form = TaskForm(instance=task)##formulario autollenado
        return render(request, 'task_detail.html',{
            'task':task,
            'form' :form
    })
    else:
        try:
            task =get_object_or_404(Task,pk=task_id,user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, 'task_detail.html',{
            'task':task,
            'form' :form,
            'error' : "Error Updating task"
            })

@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()## guarda la fecha
        task.save()
        return redirect('task')

@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form' : TaskForm
        })
    else:
        try:
            form =TaskForm(request.POST) #captura los datos de ingreso
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
        except ValueError:
            return render(request, 'create_task.html',{
            'form' : TaskForm,
            'error' : "Please provide validate data"
        })