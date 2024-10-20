from django.urls import path
from prediction import views

urlpatterns = [
    path('',views.Home,name='Home'),
    path('',views.back,name='back'),
    path('prediction',views.preditcion,name='Home')

]