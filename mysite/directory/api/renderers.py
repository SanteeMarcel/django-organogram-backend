from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer


class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return JSONRenderer()

    def get_context(self, *args, **kwargs):
        context = super(CustomBrowsableAPIRenderer, self).get_context(
            *args, **kwargs
        )
        context['display_edit_forms'] = True
        return context
