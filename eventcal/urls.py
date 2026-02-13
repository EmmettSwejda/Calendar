# urls file
from django.urls import path
from . import views




# urls for this app
urlpatterns = [
    path('', views.urlUpload, name='url-upload'),
    path('calendar/', views.calendarView, name='calendar-view'),
]