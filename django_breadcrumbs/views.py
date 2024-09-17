from bread import LazyCrumb

class BreadcrumbMixin(object):
    """
    A simple mixin system for defining the breadcrumbs 
    to  navigate complex information systems.

    To be used with Django's generic List views:
        ListView, CreateView, UpdateView, DeleteView, DetailView

    """
    breadcrumb_parents = []
    breadcrumb_current = None

    def setup(self, request, *args, **kwargs):
        self.breadcrumbs = []
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        for breadcrumb in self.breadcrumb_parents + [self.breadcrumb_current]:
            if isinstance(breadcrumb, LazyCrumb):
                self.breadcrumbs.append(breadcrumb.reverse(self.kwargs))
            else:
                self.breadcrumbs.append(breadcrumb)
        
        if self.extra_context is None:
            self.extra_context = {}
        self.extra_context['breadcrumbs'] = self.breadcrumbs
        return super().get_context_data(**kwargs)