from django.shortcuts import render, redirect
from eventcal.forms import CalendarConfigForm
from eventcal.models import CalendarConfig
from eventcal.utils import *
from datetime import date
import io
import base64

# simple form to initially get the url and get the info
def urlUplaod(request):
    template = 'url-form.html'
    

    img = Generate_Qr_Code("http://" + get_ip() + ":8000?id=second_device")

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    form = CalendarConfigForm(request.POST)

    if CalendarConfig.objects.all().count() > 0:
        return redirect(calendarView)

    if request.method == 'POST':
        if form.is_valid():
            
            form.save()
            return redirect(calendarView)

    return render(request, template , {'form': form, 'qrcode' : img_str })


# the view to see the basic calendar
def calendarView(request):
    template = 'calendar-view.html'
    today = date.today()
    month_days = get_calendar_days(today.year, today.month)
    # Always get the first configuration
    link = CalendarConfig.objects.get(id=1).url

    # Download the calendar data
    calendar_data = DownloadCalendar(link)

    # Parse the calendar info
    ParseCalendar(calendar_data)


    # Get the days of the current month
    events = Event.objects.filter(
        date__year=today.year,
        date__month=today.month
    ).order_by('date')

    month = today.strftime("%B")


    context = {
        "today": today,
        "days": month_days,
        "data": events,
        "month_name" : month
    }

    return render(request, template, context)