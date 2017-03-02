from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^appointments$', views.success, name="success"),
    url(r'^createNew$', views.createNew, name="createNew"),
    url(r'^edit/(?P<apt_id>\d+)$', views.edit, name="edit"),
    url(r'^editPage/(?P<apt_id>\d+)$', views.editPage, name="editPage"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^delete/(?P<apt_id>\d+)$', views.delete, name="delete"),
]
