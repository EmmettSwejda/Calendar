# urls file
from django.urls import path
from . import views




# urls for this app
urlpatterns = [
    path('', views.urlUplaod, name='url-upload'),
    path('calendar/', views.calendarView, name='calendar-view'),

]