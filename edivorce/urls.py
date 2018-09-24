from django.conf.urls import include, url
from django.contrib import admin
from .apps.core.views import main

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('edivorce.apps.core.urls')),
]

handler404 = main.page_not_found
handler500 = main.server_error
