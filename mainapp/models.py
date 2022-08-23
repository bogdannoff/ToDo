from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Tasks(models.Model):
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(max_length=1000)
    target_date = models.DateTimeField(null=True)
    complete = models.BooleanField(default=False)
    complete_date = models.DateTimeField(null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='images/%Y/%m/%d')
    project = models.ForeignKey('Projects', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks', kwargs={'task_id': self.pk})

    class Meta():
        verbose_name = 'Tasks_'
        verbose_name_plural = 'Tasks_'
        ordering = ['target_date', 'title']


class Projects(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects', kwargs={'project_id': self.pk})

    class Meta():
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['title']
