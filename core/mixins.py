import csv
import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchVector
from django.http import StreamingHttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from .utils import PseudoBuffer


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


class FacilitatorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    CBV mixin which makes sure user is a facilitator.
    """

    def test_func(self):
        """
        Ensure user is a facilitator.

        Returns true if user is facilitator.
        """
        return self.request.user.is_facilitator


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


class PopupTemplateMixin:

    def is_popup(self):
        return bool(self.request.GET.get('_popup'))

    def get_template_names(self):
        if self.is_popup():
            return [f"{self.template_name.split('.')[0]}_popup.html"]

        return super().get_template_names()


class PopupModelFormMixin(PopupTemplateMixin):

    def get_popup_response_data(self):
        return {}

    def form_valid(self, form):
        self.object = form.save()

        if self.is_popup():
            return TemplateResponse(
                self.request,
                'core/popup_response.html',
                {'popup_response_data': json.dumps(self.get_popup_response_data())}
            )

        return redirect(self.get_success_url())


class PopupDeleteMixin(PopupTemplateMixin):
    """Delete object.

    Taking into account popups.
    """

    def delete(self, request, *args, **kwargs):

        if self.is_popup():
            self.object = self.get_object()
            self.object.delete()

            popup_response_data = json.dumps({
                'action': 'delete_object',
            })

            return TemplateResponse(
                self.request,
                'core/popup_response.html',
                {'popup_response_data': popup_response_data}
            )

        return super().delete(request, *args, **kwargs)


class CSVResponseMixin:
    """
    A mixin for Streaming CSV response.

    To use this mixin you should define :meth:`~get_rows()` method
    """
    filename = 'export.csv'

    def get_filename(self):
        """
        Returns filename for the generated download.

        Override this to customize file name. By default this returns :attr:`~filename`
        """
        return self.filename

    def get_rows(self):
        """
        Override this method to yield list of values which will be considered as rows.
        """
        raise NotImplementedError

    def get_renderer(self):
        """This should return 'csv' for CSV response."""
        return 'csv'

    def render_csv(self):

        writer = csv.writer(PseudoBuffer())

        response = StreamingHttpResponse(
            [writer.writerow(row) for row in self.get_rows()],
            content_type="text/csv"
        )

        response['Content-Disposition'] = f'attachment; filename="{self.get_filename()}"'
        return response

    def render_to_response(self, context, **response_kwargs):
        if self.get_renderer() == 'csv':
            return self.render_csv()
        return super().render_to_response(context, **response_kwargs)


class CreatorAdminMixin:
    """
    Django admin mixin automatically assigns object creator and adds
    id, uuid, created_at and updated_at as read only fields.
    """
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


class SearchVectorFilterMixin:
    """FilterSet Mixin for text seach using Postgresql full text search."""

    def filter_search_vector(self, queryset, name, value):
        # NOTE: Ideally this should have a DB Index to avoid performance issues
        # https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/#performance

        if not value:
            return queryset

        return queryset.annotate(
            search_vector=SearchVector(*self.search_vector_fields)
        ).filter(search_vector=value)
