from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index),
    path('signup/', RegisterUser.as_view(), name='signup'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('today/', TodayView.as_view(), name='today'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    # re_path(r'tasks/(?P<year>[0-9]{4})', tasks),
    path('tasks/<int:task_id>', ShowTaskView.as_view(), name='tasks'),
    path('projects/<int:project_id>', ProjectView.as_view(), name='projects'),
    path('tasks/add', AddTask.as_view(), name='add_task'),

]