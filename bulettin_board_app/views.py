from random import shuffle

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.postgres.search import SearchVector
from django.views.generic import CreateView

from bulettin_board_app.forms import AnnoucementForm
from bulettin_board_app.models import Announcement, Photos, Category, Locations
from django.core.mail import send_mail


class IndexView(View):

    def get(self, request):
        annoucements = Announcement.objects.all()
        photos = Photos.objects.filter(announcement__in=annoucements)
        locations = Locations.objects.first()

        ctx = {
            "annoucements": annoucements,
            "photos": photos,
            "locations": locations,

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

        if len(request.FILES) != 0 and name and description and user and category and city and street and province:
            image = request.FILES['image1']
            locations = Locations.objects.create(city=city, street=street, province=province)
            annoucement = Announcement.objects.create(name=name,
                                                      description=description,
                                                      category_id=category,
                                                      locations_id=locations.id,
                                                      user_id=user.id,
                                                      )
            Photos.objects.create(img=image, announcement_id=annoucement.id)
        else:
            locations = Locations.objects.create(city=city, street=street, province=province)
            Announcement.objects.create(name=name,
                                        description=description,
                                        category_id=category,
                                        locations_id=locations.id,
                                        user_id=user.id,
                                        )

            return redirect('index')


class DetaliAnnounceIdView(View):
    template_name = "bulettin_board_app/app-details-announce.html"

    def get(self, request, id):
        annoucement = Announcement.objects.get(id=id)
        locations = Locations.objects.get(id=annoucement.locations_id)
        category = Category.objects.get(id=annoucement.category_id)
        try:
            photos = Photos.objects.get(announcement_id=id)
            ctx = {
                "annoucement": annoucement,
                "locations": locations,
                "photos": photos,
                "category": category
            }
            return render(request, self.template_name, ctx)
        except Photos.DoesNotExist:
            ctx = {
                "annoucement": annoucement,
                "locations": locations,
                "category": category
            }
            return render(request, self.template_name, ctx)


class MyAnnounceView(View):

    def get(self, request):
        user = request.user
        annoucements = Announcement.objects.filter(user_id=user.id)
        photos = Photos.objects.filter(announcement__in=annoucements)
        if not annoucements:
            info = "Nie masz jeszcze żadnych ogłoszeń"
        else:
            info = "Moje ogłoszenia"
        ctx = {
            "annoucements": annoucements,
            "photos": photos,
            "info": info,
        }
        return render(request, "bulettin_board_app/index.html", ctx)


class DeleteView(View):

    def get(self, request, id):
        annoucement = Announcement.objects.get(id=id)
        annoucement.delete()
        return redirect("my_announce")


class EditView(View):
    template_name = "bulettin_board_app/app-edit-announce.html"

    def get(self, request, id):
        annoucement = Announcement.objects.get(id=id)
        locations = Locations.objects.get(id=annoucement.locations_id)
        category = Category.objects.get(id=annoucement.category_id)
        try:
            photos = Photos.objects.get(announcement_id=id)
            ctx = {
                "annoucement": annoucement,
                "locations": locations,
                "photos": photos,
                "category": category
            }
            return render(request, self.template_name, ctx)
        except Photos.DoesNotExist:
            ctx = {
                "annoucement": annoucement,
                "locations": locations,
                "category": category
            }
            return render(request, self.template_name, ctx)

    def post(self, request, id):

        annoucement = Announcement.objects.get(id=id)
        locations = Locations.objects.get(id=annoucement.locations_id)
        photos = Photos.objects.get(announcement_id=id)

        annoucement.name = request.POST.get("name")
        annoucement.description = request.POST.get('description')
        annoucement.user_id = request.user.id
        annoucement.category_id = request.POST.get('category')
        locations.city = request.POST.get("city")
        locations.street = request.POST.get("street")
        locations.province = request.POST.get("province")

        if len(request.FILES) != 0:
            photos.img = request.FILES['image1']
            photos.announcement_id = annoucement.id
            annoucement.save()
            locations.save()
            photos.save()

        else:
            annoucement.save()
            locations.save()

        return redirect('details_announce', id=id)


class SendEmailView(View):

    def get(self, request, id):
        annoucement = Announcement.objects.get(id=id)
        return render(request, 'bulettin_board_app/app-send-email.html', {'annoucement': annoucement})

    def post(self, request, id):
        annoucement = Announcement.objects.get(id=id)
        email_sender = request.POST.get("email")
        topic = request.POST.get("topic")
        message = request.POST.get("desription")
        email_announce = "tomizdebski@gmail.com"
        send_mail(topic, message, email_sender, [email_announce], fail_silently=False)

        return redirect("details_announce", id=annoucement.id)


class ByCategoryView(View):

    def get(self, request, id_category):
        annoucements = Announcement.objects.filter(category_id=id_category)
        photos = Photos.objects.filter(announcement__in=annoucements)
        category = Category.objects.get(id=id_category)

        ctx = {
            "annoucements": annoucements,
            "photos": photos,
            "category": category,
        }

        return render(request, "bulettin_board_app/app-view-by-category.html", ctx)


class SearchView(View):

    def get(self):
        ...

    def post(self, request):
        search_query = request.POST.get('search')
        result = Announcement.objects.annotate(search=SearchVector('name', 'description'), ).filter(search=search_query)
        photos = Photos.objects.filter(announcement__in=result)
        ctx = {
            "annoucements": result,
            "photos": photos,
        }
        return render(request, "bulettin_board_app/app-search.html", ctx)
