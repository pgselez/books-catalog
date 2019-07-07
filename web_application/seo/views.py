from django.shortcuts import render
from .models import RobotsTxt


# Create your views here.

def robots_txt_view(request):
    robots = RobotsTxt.objects.get()
    context = {'robots': robots}
    return render(request, 'robots.txt', context, content_type="text/plain")
