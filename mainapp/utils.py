from urllib.parse import urlparse

from mainapp.models import Tasks


class TaskMixin:

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user).select_related('project').order_by('target_date')

    def get_form_kwargs_user(self, **kwargs):
        kwargs['initial']['user'] = self.request.user
        return kwargs

    def get_previous_page(self):
        nextp = self.request.GET.get('nextp')
        if not nextp:
            parsed = urlparse(self.request.META['HTTP_REFERER'])
            return parsed.path + '?' + parsed.query
        return nextp
