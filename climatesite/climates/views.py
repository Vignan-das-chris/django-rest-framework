from django.shortcuts import render

#login and logout
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# djangorest-weatherclimateresponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from climates.models import Climate
from climates.serializers import ClimateSerializer


# logginin

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'], password=cd['1234'])
            if user is not None:
                login(request, user)
                return HttpResponse('Authenticated')
            else:
                return HttpResponse('disabled')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'climates/login.html', {'form': form})

# weather information


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def climate_list(request):
    if request.method == 'GET':
        climates = Climate.objects.all()
        climates_serializer = ClimateSerializer(climates, many=True)
        return JSONResponse(climates_serializer.data)

    elif request.method == 'POST':
        climate_data = JSONParser.parse(request)
        climate_serializer = ClimateSerializer(data=climate_data)
        if climate_serializer.is_valid():
            climate_serializer.save()
            return JSONResponse(climate_serializer.data,
                                status=status.HTTP_201_CREATED)
    return JSONResponse(climate_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def climate_detail(request, name):
    try:
        climate = Climate.objects.get(name=name)
    except Climate.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        climate_serializer = ClimateSerializer(climate)
        return JSONResponse(climate_serializer.data)

    elif request.method == 'PUT':
        climate_data = JSONParser().parse(request)
        climate_serializer = ClimateSerializer(climate, data=climate_data)
        if climate_serializer.is_valid():
            climate_serializer.save()
            return JSONResponse(climate_serializer.data)
        return JSONResponse(climate_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        climate.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
