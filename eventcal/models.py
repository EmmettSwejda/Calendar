from django.db import models


# Describes an event to be shown on the calendar
class Event(models.Model):
    uid = models.CharField()
    title = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    allday = models.BooleanField(default=False)

# Holds the url to the webcal file
class CalendarConfig(models.Model):
    url = models.URLField()
