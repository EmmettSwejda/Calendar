import requests
from eventcal.models import Event
from ics import Calendar


# Utilities
def DownloadCalendar(webcal_link):
    if webcal_link.startswith('https://'):
        webcal_link = webcal_link.replace('webcal://', 'https://')

    try:
        response = requests.get(webcal_link, verify=True)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Downloading calendar data failed: {e}")
        return None


# Parse calendar information and add to the database
def ParseCalendar(data):
    cal = Calendar(data.decode('utf-8'))
    # Not optimal but since speed is not required for this application
    #   just wipe the entire table and re add all events
    #   this solves the issue of figuring out what events have been deleted
    Event.objects.all().delete()

    for even in cal.events:
        new_event = Event(uid=even.uid, title=even.name, notes=even.description, date=even.begin.date(),
                          start=even.begin.time(), end=even.end.time())
        new_event.save()
