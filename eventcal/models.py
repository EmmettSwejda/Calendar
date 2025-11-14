from django.db import models


# Describes an event to be shown on the calendar
class Event(models.Model):
    title = models.CharField(max_length=100)
    notes = models.TextField()
    Start = models.TimeField()
    end = models.TimeField()
    allday = models.BooleanField(default=False)



# Describes a day on the calendar
class Day(models.Model):
    Date = models.DateField()
    events = models.ManyToManyField(Event)



# Holds the url to the webcal file
class CalendarConfig(models.Model):
    url = models.URLField()
