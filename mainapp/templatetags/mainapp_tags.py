from datetime import datetime

from django import template
from django.db import connection

from mainapp.models import *


register = template.Library()


# @register.simple_tag(name='tag_projects')
# def get_projects():
#     return Projects.objects.all()
#
#
# @register.simple_tag(name='tag_is_equals')
# def is_equals(request, obj):
#     return (str(request)==str(obj))

@register.simple_tag(name='get_url_params', takes_context=True)
def get_url_params(context, page):
    url_params = {x: y for x, y in context.request.GET.items()}
    url_params['page'] = page
    return '&'.join([f'{key}={val}' for key, val in url_params.items()])


@register.inclusion_tag(name='tag_get_menu', filename='mainapp/left_menu.html', takes_context=True)
def get_menu(context):

    request = context['request']
    filter = ''
    if request.GET.get('date') == 'today':
        filter = request.GET['date']
    elif request.GET.get('project') is not None:
        filter = request.GET['project']

    query_text = """
        SELECT 
            COUNT(DISTINCT t.id) AS undone_all,
            COUNT(DISTINCT 
                CASE 
                    WHEN t.target_date <= %s or t.target_date is null
                    THEN t.id
                END    
            ) AS undone_today
        FROM mainapp_tasks AS t 
        WHERE t.user_id = %s
            and not t.complete
        """

    with connection.cursor() as cursor:
        cursor.execute(query_text, [datetime.today(), request.user.id])
        total = cursor.fetchall()

    menulist = [
            {'name': 'All', 'active': filter == '', 'undone_count': total[0][0], 'url_name': reverse('tasks')},
            {'name': 'Today', 'active': filter == 'today', 'undone_count': total[0][1], 'url_name': reverse('tasks')+f'?date=today'},
    ]

    queryset =Projects.objects.raw(
        """
        SELECT 
            p.id AS id,
            p.title AS title,
            COUNT(DISTINCT t.id) AS undone
        FROM mainapp_projects AS p 
            LEFT JOIN mainapp_tasks AS t 
                ON p.id=t.project_id
                    and not t.complete
                    and t.user_id = %s
        WHERE p.user_id = %s
        GROUP BY 
            p.id,
            p.title
        ORDER BY p.title
        """,
        [request.user.id, request.user.id]
    )
    projects = [{'name': item.title,
                 'active': filter == str(item.id),
                 'undone_count': item.undone,
                 'url_name': reverse('tasks')+f'?project={item.id}'
                 } for item in queryset]

    context = {
        'menulist': menulist,
        'projects': projects,
    }
    return context
