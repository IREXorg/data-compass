"""
datacompass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/3.0/topics/http/urls/

Adding views or URL
-------------------

Adding function views

1. Add an import:  ``from my_app import views``
2. Add a URL to urlpatterns:  ``path('', views.home, name='home')``

Adding class-based views

1. Add an import:  ``from other_app.views import Home``
2. Add a URL to urlpatterns:  ``path('', Home.as_view(), name='home')``

Including another URLconf

1. Import the include() function: ``from django.urls import include, path``
2. Add a URL to urlpatterns:  ``path('blog/', include('blog.urls'), namespace='blog')``

"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from apps.respondents.views import SendInviteView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('projects/', include('apps.projects.urls', namespace='projects')),
    path('surveys/', include('apps.surveys.urls', namespace='surveys')),
    path('respondents/', include('apps.respondents.urls', namespace='respondents')),
    path('responses/', include('apps.responses.urls', namespace='responses')),
    path('summernote/', include('django_summernote.urls')),
    path('invitations/send-invite/', SendInviteView.as_view()),
    path('invitations/', include('invitations.urls', namespace='invitations')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', '')
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', '')
admin.site.site_title = getattr(settings, 'ADMIN_SITE_NAME', '')
