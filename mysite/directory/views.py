from django.http import HttpResponse


def index(request):
    return HttpResponse("You're off to a good start, but there's nothing to see here. We're only using the API.")
