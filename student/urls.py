from . import views
from django.urls import path,include

urlpatterns = [
    path('login',views.login,name="login"),
    path('qrscan',views.qrscan,name="qrscan"),
    path('register',views.register,name="register"),
    path('upload',views.upload,name="upload"),
]