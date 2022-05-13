from . import views
from django.urls import path, include,re_path

app_name = 'enSentiment'


urlpatterns = [
    path('', views.home, name='home'),
    path('login',views.login, name='login'),
    path('register',views.register, name='register'),
    path('logout',views.logout, name='logout'),
    path('result',views.result, name='result'),
    re_path(r'^result/(?P<id>\d+)/$', views.result ,name='result'),
    re_path(r'^del_result/(?P<id>\d+)/$', views.del_result ,name='del_result'),
    path('allTweets',views.allTweets, name='allTweets'),
    path('myresults',views.myresults, name='myresults'),
    path('profile',views.profile, name='profile'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('ajax/getAnalysis',views.getAnalysis, name='getAnalysis'),
]
