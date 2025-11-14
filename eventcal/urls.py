# urls file
from django.urls import path
from . import views




# urls for this app
urlpatterns = [
    path('', views.eventcal, name='eventcal'),
    path('eventcal/', views.eventcal, name='eventcal'),
]