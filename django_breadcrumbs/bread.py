from django.urls import reverse_lazy, reverse
from django.utils.functional import lazy

class Crumb(object):
    def __init__(self, label, url, current=False):
        self.label = label
        self.url = url
        self.current = current

class LazyCrumb(Crumb):
    """ Renders a breadcrumb on page load to reflect 
        the current model being viewed.
    """
    def __init__(self, label, url, slugs=[], model=None, current=False):
        """
            label: (str|method)
            url: (str) the named url
            slugs: (list)
            model: (object)
            current: (bool)
        """
        super().__init__(label, url)
        self.slugs = slugs
        self.model = model
        self.current = current

    def reverse(self, kwargs, object=None):
        args={}
        for slug in self.slugs:
            if ':' in slug:
                parts = slug.split(':')
                args[parts[1]] = kwargs.get(parts[0])
            else:
                args[slug] = kwargs.get(slug)
        url = None
        if self.url is not None:
            url = reverse(self.url, kwargs=args)
        label = self.label
        obj = args
        if self.model:
            obj = object
            if obj is None:
                obj = self.model.objects.get(**args)
        if callable(self.label):
            label = self.label(obj)
        else:
            label = label.format(**obj)
        return Crumb(label, url, current=self.current)