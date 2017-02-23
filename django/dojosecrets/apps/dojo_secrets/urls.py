from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^secrets/$', views.secrets, name="secrets"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^postsecret$', views.postsecret, name="postsecret"),
    url(r'^likes/(?P<message>\d)$', views.likes, name="like"),
    url(r'^popular$', views.popular, name="like")
]
