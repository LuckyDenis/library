from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    url("^books/$", views.BookList.as_view(), name="books"),
    url("^books/(?P<pk>\d+)/$", views.BookInfo.as_view(), name='book-info'),
]
