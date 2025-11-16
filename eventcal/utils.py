import calendar
import datetime
import requests
from eventcal.models import Event
from ics import Calendar

# Utilities

# Download the calendar based on the webcal link
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
                          start=even.begin.time(), end=even.end.time(), allday=even.all_day)

        new_event.save()



# Generate all days in the calendar month
# as well as any days that might be missing from
#   the starting week
#   or ending week
def get_calendar_days(year, month):
    first_day = datetime.date(year, month, 1)

    _, num_days = calendar.monthrange(year, month)
    last_day = datetime.date(year, month, num_days)

    first_weekday = (first_day.weekday() + 1) % 7
    last_weekday = (last_day.weekday() + 1) % 7

    start_date = first_day - datetime.timedelta(days=first_weekday)
    end_date = last_day + datetime.timedelta(days=(6 - last_weekday))

    # Generate all days
    days = []
    current = start_date

    while current <= end_date:
        # mark if its a real date or not
        # so it can be made dim
        days.append((
            current,
            current.month == month,
        ))
        current += datetime.timedelta(days=1)

    return days
