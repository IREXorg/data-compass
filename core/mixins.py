class PageTitleMixin:
    """
    Passes page_title and active_tab into context data.
    """
    page_title = None
    active_tab = None

    def get_page_title(self):
        """Override this for dynamic page_title."""
        return self.page_title

    def get_active_tab(self):
        """Override this for dynamic active_tab."""
        return self.active_tab

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('page_title', self.get_page_title())
        ctx.setdefault('active_tab', self.get_page_title())
        return ctx


class PageMixin(PageTitleMixin):
    """
    Page Mixin for Class Based Views.

    Adds :attr:`~back_url_path` to context data.
    """

    #: Back URL path, for example when user clicks back button on a form.
    back_url_path = None

    def get_back_url_path(self):
        """Override this for dynamic back_path."""
        return self.back_url_path or self.request.META['HTTP_REFERER']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('back_url_path', self.get_back_url_path())
        return ctx
