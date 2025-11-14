from django.http import HttpResponse
from django.template import loader

# Create your views here.

def eventcal(request):
    template = loader.get_template("base.html")
    return HttpResponse(template.render())