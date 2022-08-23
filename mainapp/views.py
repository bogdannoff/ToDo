import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import *
from .forms import *
from .utils import DataMixin


def index(request, num=None):
    task_list = Tasks.objects.all().order_by('id')
    paginator = Paginator(task_list,5)
    context = {
        'page_obj': paginator.get_page(request.GET.get('page')),
    }

    return render(request, 'mainapp/maintasks.html', context=context)


class TasksView(DataMixin, ListView):
    model = Tasks
    template_name = 'mainapp/tasks.html'
    context_object_name = 'tasklist'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_context(context, title='All my tasks')
        return context

    def get_queryset(self):
        return Tasks.objects.all().select_related('project')


class TodayView(ListView):
    model = Tasks
    template_name = 'mainapp/tasks.html'
    context_object_name = 'tasklist'
    paginate_by = 5

    def get_queryset(self):
        return Tasks.objects.filter(Q(target_date__lt=+datetime.timedelta(days=1)) | Q(target_date=None))\
            .order_by('target_date')


class ProjectView(ListView):
    model = Tasks
    template_name = 'mainapp/tasks.html'
    context_object_name = 'tasklist'
    paginate_by = 5

    def get_queryset(self):
        return Tasks.objects.filter(project=self.kwargs['project_id']).order_by('target_date')


def projects(request, project_id):
    context = {
        'tasklist': Tasks.objects.filter(project=project_id).order_by('target_date'),
    }
    return render(request, 'mainapp/tasks.html', context=context)


class ShowTaskView(DetailView):
    model = Tasks
    template_name = 'mainapp/task.html'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'


class AddTask(LoginRequiredMixin, CreateView):
    form_class = AddTaskForm
    template_name = 'mainapp/add_task.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('tasks')

# def add_task(request):
#     if request.method == 'POST':
#         form = AddTaskForm(request.POST)
#         if form.is_valid():
#             # Tasks.objects.create(**form.cleaned_data)
#             form.save()
#             return redirect('tasks')
#         print(form)
#     else:
#         form = AddTaskForm()
#     return render(request, 'mainapp/add_task.html', {'form': form})


class RegisterUser(DataMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'mainapp/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_context(context, title='Sign Up')
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('tasks')


class LoginUser(DataMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'mainapp/login.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_context(context, title='login')
        return context

    def get_success_url(self):
        return reverse_lazy('tasks')


def logout_user(request):
    logout(request)
    return redirect('login')