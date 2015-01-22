from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.user_login, name='index'),
	url(r'^register/$', views.register, name='index'),
    url(r'^newfeed/$', views.newfeed, name='index'),
    url(r'^fav/(?P<feed_id>\d+)/$', views.favorite, name='details'),
	url(r'^unfav/(?P<feed_id>\d+)/$', views.unfavorite, name='details'),
    url(r'^starred/$', views.starred, name='index'),

    url(r'^account/$', views.account, name='index'),
    url(r'^logout/$', views.user_logout, name='index'),
    # url(r'^change_password/$', views.change_password, name='index'),
 #  url(r'^change_email/$', views.change_email, name='index'),
 #  url(r'^change_college/$', views.change_college, name='index'),
)