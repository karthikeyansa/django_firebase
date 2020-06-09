from django.urls import path
from . import views
urlpatterns = [
    path('',views.signin,name = 'signin'),
    path('welcome/<str:email>/',views.welcome,name = 'welcome'),
    path('logout/',views.logout,name = 'logout'),
    path('signup/',views.newuser,name = 'newuser'),
    path('post/',views.post_report,name = 'post_report'),
    path('path/',views.check_report,name = 'check_report'),
]