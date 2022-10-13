import json
from datetime import datetime

import googlemaps
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from bulettin_board_app.models import Locations


def home(request):
    context = {}
    return render(request, 'google/home.html', context)


def geocode(request):
    locations = Locations.objects.all()
    context = {
        'locations': locations,
    }
    return render(request, 'google/geocode.html', context)


def geocode_locations(request, pk):
    locations = Locations.objects.get(id=pk)
    # check whether we have the data in the database that we need to calculate the geocode
    if locations.street and locations.country and locations.zipcode and locations.city and locations.province != None:
        # creating string of existing location data in database
        adress_string = str(locations.street) + ", " + str(locations.zipcode) + ", " + str(locations.city) + ", " \
                        + str(locations.country) + ", " + str(locations.province)
        print(adress_string)

        # geocode the string
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        intermediate = json.dumps(gmaps.geocode(str(adress_string)))
        intermediate2 = json.loads(intermediate)
        latitude = intermediate2[0]['geometry']['location']['lat']
        longitude = intermediate2[0]['geometry']['location']['lng']
        print(latitude)
        print(longitude)
        # save the lat and long in our database
        locations.latitude = latitude
        locations.longitude = longitude
        locations.save()
        return redirect('geocode')
    else:
        return redirect('geocode')


def distance(request):
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
    now = datetime.now()
    calculate = json.dumps(gmaps.distance_matrix("Rat Verlegh Stadion",
                                                 "Breda Station",
                                                 mode="driving",
                                                 departure_time=now))
    calculate2 = json.loads(calculate)

    result = calculate2
    distance = calculate2['rows'][0]['elements'][0]['distance']['value']
    duration = calculate2['rows'][0]['elements'][0]['duration']['text']

    context = {
        'result': result,
        'distance': distance,
        'duration': duration
    }
    return render(request, 'google/distance.html', context)


def calculate_distance(request, pk, pk2):
    location1 = Locations.objects.get(id=pk)
    location2 = Locations.objects.get(id=pk2)

    result = Locations.objects.all()
    context = {
        'result': result,
    }
    return render(request, 'google/distance.html', context)


def map(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key': key,
        'id': id,
    }
    return render(request, 'google/map.html', context)


def mydata(request):

    result_list = list(Locations.objects \
                       .exclude(latitude__isnull=True) \
                       .exclude(longitude__isnull=True) \
                       .exclude(latitude__exact='') \
                       .exclude(longitude__exact='') \
                       .values('id',
                               'name',
                               'latitude',
                               'longitude',
                               'city',
                               'country',
                               ))

    return JsonResponse(result_list, safe=False)
