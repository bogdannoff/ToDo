
class DataMixin:

    def get_context(self, context, **kwargs):
        for x, val in kwargs.items():
            context[x] = val
        return context
