from django.shortcuts import render, redirect
from eventcal.forms import CalendarConfigForm


def urlUplaod(request):
    template = 'url-form.html'
    form = CalendarConfigForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(calendarView)

    return render(request, template , {'form': form})


# the view to see the basic calendar
def calendarView(request):
    template = 'calendar-view.html'


    return render(request, template)