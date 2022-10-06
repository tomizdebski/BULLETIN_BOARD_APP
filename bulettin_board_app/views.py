from random import shuffle

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView

from bulettin_board_app.forms import AnnoucementForm
from bulettin_board_app.models import Announcement, Photos, Category, Locations


class IndexView(View):
    def get(self, request):
        annoucements = Announcement.objects.order_by('-id')
        photos = Photos.objects.filter(announcement__in=annoucements)

        ctx = {
            "annoucements": annoucements,
            "photos": photos
        }

        return render(request, "bulettin_board_app/index.html", ctx)


class AddAnnounceView(View):
    def get(self, request):
        return render(request, "bulettin_board_app/app-add-annouce.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get('description')
        user = request.user
        category = request.POST.get('category')
        city = request.POST.get("city")
        street = request.POST.get("street")
        province = request.POST.get("province")

        if len(request.FILES) != 0:
            image = request.FILES['image1']
            locations = Locations.objects.create(city=city, street=street, province=province)
            annoucement = Announcement.objects.create(name=name,
                                                      description=description,
                                                      category_id=category,
                                                      locations_id=locations.id,
                                                      user_id=user.id,
                                                      )
            photos = Photos.objects.create(img=image, announcement_id=annoucement.id)


            return redirect('index')


class DetaliAnnounceIdView(View):
    template_name = "bulettin_board_app/app-details-announce.html"

    def get(self, request, id):
        annoucement = Announcement.objects.get(id=id)
        locations = Locations.objects.get(id=annoucement.locations_id)
        photos = Photos.objects.get(announcement_id=id)
        category = Category.objects.get(id=annoucement.category_id)
        ctx = {
            "annoucement": annoucement,
            "locations": locations,
            "photos": photos,
            "category": category
        }
        return render(request, self.template_name, ctx)


class MyAnnounceView(View):
    def get(self, request):
        user = request.user
        annoucements = Announcement.objects.filter(user_id=user.id)
        photos = Photos.objects.filter(announcement__in=annoucements)

        ctx = {
            "annoucements": annoucements,
            "photos": photos
        }

        return render(request, "bulettin_board_app/index.html", ctx)
