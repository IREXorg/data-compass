class PageTitleMixin(object):
    """
    Passes page_title into context.
    Dynamic page titles are possible by overriding ``get_page_title`` method.
    """
    page_title = None
    active_tab = None

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('page_title', self.get_page_title())
        return ctx
