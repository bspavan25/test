from teacher import views
from django.urls import path,include

urlpatterns = [
    path('home',views.home,name="home"),
    path('',views.home,name="home"),
    path('generateqr',views.generateqr,name='generateqr'),
    path('teacher',views.teacher,name='teacher'),

]