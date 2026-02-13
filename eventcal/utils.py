import calendar
import datetime
import requests
import qrcode
import socket
import os
from django.conf import settings
from eventcal.models import Event
from icalevents.icalevents import events
from datetime import timedelta
from io import BytesIO  # This can be removed if not used elsewhere

# Utilities

def Generate_Qr_Code(link):
    img = qrcode.make(link)
    name = "img.png" 
    path = os.path.join(settings.MEDIA_ROOT, "img.png")
    img.save(path)
    return img

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 8.8.8.8 is Google DNS; the port doesn't matter (80)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

# Download the calendar based on the webcal link
def DownloadCalendar(webcal_link):
    if webcal_link.startswith('webcal://'):
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
    # Not optimal but since speed is not required for this application
    #   just wipe the entire table and re add all events
    #   this solves the issue of figuring out what events have been deleted
    Event.objects.all().delete()

    # Define a reasonable range to expand recurrences (adjust as needed)
    start_range = datetime.datetime.now() - timedelta(days=365)  # 1 year in the past
    end_range = datetime.datetime.now() + timedelta(days=365 * 5)  # 5 years in the future

    # Parse and expand events, including recurrences
    expanded_events = events(string_content=data, start=start_range, end=end_range,fix_apple=True)

    for even in expanded_events:
        # Create a unique UID for each occurrence to avoid potential uniqueness conflicts
        occurrence_uid = f"{even.uid}_{even.start.date().isoformat()}"

        new_event = Event(
            uid=occurrence_uid,
            title=even.summary,
            notes=even.description,
            date=even.start.date(),
            start=even.start.time(),
            end=even.end.time(),
            allday=even.all_day
        )

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