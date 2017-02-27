from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^wish_items/create$', views.create, name="create"),
    url(r'^wish_items/new_item$', views.new, name="new_item"),
    url(r'^delete/(?P<wish_id>\d+)$', views.delete, name="delete"),
    url(r'^remove/(?P<wish_id>\d+)$', views.remove, name="remove"),
    url(r'^addto/(?P<wish_id>\d+)$', views.addto, name="addto"),
]
