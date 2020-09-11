from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url='/catalog/')),
    path('catalog/', include('catalog.urls')),
    path('admin/', admin.site.urls),
]
