from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from movie.core import tmdb
from movie.core import twitter
from movie.core import regression
from movie.core import graph
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
    url(r'^graphs/2d$', views.graph2d, name='graph2d'),
    url(r'^graphs/3d$', views.graph3d, name='graph3d'),
    url(r'^comparison/$', views.comparisonTable, name='comparisonTable'),

    ##API##
    url(r'^getupcoming/$', tmdb.get_upcoming, name='getupcoming'),
    url(r'^getsentiment/$', twitter.get_sentiment, name='getsentiment'),
    url(r'^getmoviedetails/$', tmdb.get_details, name='getmoviedetails'),
    url(r'^regression/$', regression.calculate, name='calcregression'),
    url(r'^linearReg/$', regression.linearModel, name='linearReg'),

    ##GRAPHS##
    url(r'^graphs/3d.png/$', graph.plot3d, name='plot3d'),
    url(r'^graphs/2d.png/$', graph.plot2d, name='plot2d'),

]