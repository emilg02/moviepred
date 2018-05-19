from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from movie.core import tmdb
from movie.core import twitter
from movie.core import regression

urlpatterns = [
    ##VIEWS##
    path('', views.index, name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^new/$', views.new, name='new'),
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^details/$', views.details, name='details'),
    url(r'^result/$', views.result, name='result'),
    ##API##
    url(r'^getupcoming/$', tmdb.get_upcoming, name='getupcoming'),
    url(r'^getsentiment/$', twitter.get_sentiment, name='getsentiment'),
    url(r'^getmoviedetails/$', tmdb.get_details, name='getmoviedetails'),
    url(r'^regression/$', regression.calculate, name='calcregression'),

]