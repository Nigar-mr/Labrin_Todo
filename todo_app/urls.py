from django.conf.urls import url
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', ListView.as_view(), name='list'),
    path('login/', AuthLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('add/', AddView.as_view(), name='add'),
    path('sharedlist/', ShareListView.as_view(), name='shared-list'),
    path('delete/<int:pk>/delete/', PostDeleteView.as_view(), name="delete"),

]