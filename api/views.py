from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from eventcal.models import CalendarConfig, Event
from eventcal.utils import DownloadCalendar, ParseCalendar



class CalendarDataAPIView(APIView):

    def get(self, request):

        today = date.today()

        link = CalendarConfig.objects.get(id=1).url
        calendar_data = DownloadCalendar(link)
        ParseCalendar(calendar_data)

        events = Event.objects.filter(
            date__year=today.year,
            date__month=today.month
        ).order_by('date')

        return Response({
            "events": list(events.values())
        })