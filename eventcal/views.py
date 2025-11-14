from django.shortcuts import render, redirect
from eventcal.forms import CalendarConfigForm
from eventcal.models import CalendarConfig, Day
from datetime import date

# simple form to initially get the url and get the info
def urlUplaod(request):
    template = 'url-form.html'
    form = CalendarConfigForm(request.POST)

    if CalendarConfig.objects.all().count() > 0:
        return redirect(calendarView)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(calendarView)

    return render(request, template , {'form': form})


# the view to see the basic calendar
def calendarView(request):
    template = 'calendar-view.html'
    today = date.today()

    # Get the days of the current month
    days = Day.objects.filter(
        date__year=today.year,
        date__month=today.month
    )
    month = date.today().strftime("%B")

    # Store all day info in the data list
    data = []

    for day in days:
        data.append([day, day.events.all()])

    context = {
        "data": data,
        "month_name" : month
    }

    return render(request, template, context)