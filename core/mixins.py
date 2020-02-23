from django.shortcuts import redirect


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
        return self.back_url_path or self.request.META.get('HTTP_REFERER')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('back_url_path', self.get_back_url_path())
        return ctx


class InlineFormsetMixin:
    """
    Inline Formset mixin for class based views.
    """

    def get_formset(self, form_class=None):
        """Construct and return a formset instance."""
        if form_class is None:
            form_class = self.formset_class
        return form_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        """Returns argumnets to be used for instatiating the formset."""
        kwargs = {}

        if self.object:
            kwargs['instance'] = self.object

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        """save forms and redirect to success URL"""
        self.object = form.save()
        formset.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, formset):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
