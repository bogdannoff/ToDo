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
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *
from .forms import *
from .utils import TaskMixin


class TasksView(LoginRequiredMixin,
                TaskMixin,
                ListView):
    model = Tasks
    template_name = 'mainapp/tasks.html'
    context_object_name = 'tasklist'
    login_url = '/login/'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('date') == 'today':
            return queryset.filter(Q(target_date__lt=datetime.date.today()+datetime.timedelta(days=1)) | Q(target_date=None), complete=False)
        elif self.request.GET.get('project') is not None:
            return queryset.filter(project=self.request.GET['project'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['url_params'] = {x: y for x, y in self.request.GET.items()}
        return context


class DetailTaskView(LoginRequiredMixin,
                     TaskMixin,
                     UpdateView):
    form_class = DetailTaskForm
    model = Tasks
    template_name = 'mainapp/add_task.html'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.success_url = super().get_previous_page()

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        return super().get_form_kwargs_user(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse('update_task',
                                        kwargs={'task_id': context['object'].pk}) +\
                                (f'?nextp={self.success_url}' if self.success_url else '')
        context['delete_action_url'] = reverse('delete_task',
                                        kwargs={'task_id': context['object'].pk}) +\
                                (f'?nextp={self.success_url}' if self.success_url else '')
        context['delete_action'] = True
        context['action_name'] = 'Save'
        context['title'] = 'Task'
        return context


class AddTaskView(LoginRequiredMixin,
                  TaskMixin,
                  CreateView):
    form_class = AddTaskForm
    template_name = 'mainapp/add_task.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.success_url = super().get_previous_page()

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        return super().get_form_kwargs_user(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse('add_task') +\
                                (f'?nextp={self.success_url}' if self.success_url else '')
        context['action_name'] = 'Add'
        context['title'] = 'New task'
        return context


class DeleteTaskView(LoginRequiredMixin,
                  TaskMixin,
                  DeleteView):
    # form_class = AddTaskForm
    template_name = 'mainapp/confirm_delete.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.success_url = super().get_previous_page()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse('delete_task',
                                        kwargs={'task_id': context['object'].pk}) +\
                                (f'?nextp={self.success_url}' if self.success_url else '')
        # context['action_name'] = 'Add'
        context['title'] = 'Delete task'
        return context


class AddProjectView(LoginRequiredMixin,
                     TaskMixin,
                     CreateView):
    form_class = AddProjectForm
    template_name = 'mainapp/add_project.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.success_url = super().get_previous_page()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse('add_project') +\
                                (f'?nextp={self.success_url}' if self.success_url else '')
        context['action_name'] = 'Add'
        context['title'] = 'New project'
        return context


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'mainapp/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context = self.get_context(context, title='Sign Up')
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('tasks')


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'mainapp/login.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context = self.get_context(context, title='login')
        return context

    def get_success_url(self):
        return reverse_lazy('tasks')


def logout_user(request):
    logout(request)
    return redirect('login')