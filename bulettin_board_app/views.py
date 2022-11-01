import json
import googlemaps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.postgres.search import SearchVector
from BulettinBoard import settings
from bulettin_board_app.models import Announcement, Photos, Category, Locations, Watching
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(View):

    def get(self, request):
        """
        The function displays the home page
        :param request:
        :return: render page index.html
        """
        annoucements = Announcement.objects.all()
        paginator = Paginator(annoucements, 6)
        page = request.GET.get('page')
        photos = Photos.objects.filter(announcement__in=annoucements)
        locations = Locations.objects.all()

        ctx = {
            "annoucements": annoucements,
            "photos": photos,
            "locations": locations,

        }

        return render(request, "bulettin_board_app/index.html", ctx)


class AddAnnounceView(LoginRequiredMixin, View):

    def get(self, request):
        """
        The function displays page app-add-annouce.html
        :param request:
        :return: render app-add-annouce.html
        """
        return render(request, "bulettin_board_app/app-add-annouce.html")

    def post(self, request):
        """
        The function add annouce using the post method
        :param request:
        :return: if correct, it redirects to index.html if not it redirect app-add-annouce.html
        """
        name = request.POST.get("name")
        description = request.POST.get('description')
        user = request.user
        category = request.POST.get('category')
        city = request.POST.get("city")
        street = request.POST.get("street")
        province = request.POST.get("province")
        zipcode = request.POST.get("zipcode")
        country = request.POST.get("country")

        if name and description and category and city and street and province and zipcode and country:

            if len(request.FILES) != 0:
                image = request.FILES['image1']
                # google-maps- geocode - longtitude and latitude
                adress_string = str(street) + ", " + str(zipcode) + ", " + str(city) + ", " \
                                + str(country) + ", " + str(province)
                gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
                intermediate = json.dumps(gmaps.geocode(str(adress_string)))
                intermediate2 = json.loads(intermediate)
                latitude = intermediate2[0]['geometry']['location']['lat']
                longitude = intermediate2[0]['geometry']['location']['lng']

                locations = Locations.objects.create(city=city,
                                                     street=street,
                                                     province=province,
                                                     zipcode=zipcode,
                                                     country=country,
                                                     latitude=latitude,
                                                     longitude=longitude,
                                                     )

                annoucement = Announcement.objects.create(name=name,
                                                          description=description,
                                                          category_id=category,
                                                          locations_id=locations.id,
                                                          user_id=user.id,
                                                          )
                Photos.objects.create(img=image, announcement_id=annoucement.id)
                return redirect('index')
            else:
                locations = Locations.objects.create(city=city,
                                                     street=street,
                                                     province=province,
                                                     zipcode=zipcode,
                                                     country=country)
                Announcement.objects.create(name=name,
                                            description=description,
                                            category_id=category,
                                            locations_id=locations.id,
                                            user_id=user.id,
                                            )

                return redirect('index')
        else:
            return render(request, 'bulettin_board_app/app-add-annouce.html', {'error': 'Wypełnij poprawnie formularz'})


class DetailAnnounceIdView(View):
    template_name = "bulettin_board_app/app-details-announce.html"

    def get(self, request, id):
        """
        The functions displays an announce with the given id
        :param request:
        :param id:
        :return: render app-details-announce.html
        """
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


class MyAnnounceView(LoginRequiredMixin, View):

    def get(self, request):
        """
        The functions displays an my announce
        :param request:
        :return: render app-my-announce.html
        """
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
        return render(request, "bulettin_board_app/app-my-announce.html", ctx)


class DeleteView(LoginRequiredMixin, View):

    def get(self, request, id):
        """
        The functions delete announce with the given id
        :param request:
        :param id:
        :return: render app-delete-modal.html
        """
        annoucement = Announcement.objects.get(id=id)
        return render(request, "bulettin_board_app/app-delete-modal.html", {'annoucement': annoucement})

    def post(self, request, id):
        """
        The functions delete announce with the given id
        :param request:
        :param id:
        :return: redirect to my_announce
        """
        annoucement = Announcement.objects.get(id=id)
        annoucement.delete()
        return redirect("my_announce")


class EditView(LoginRequiredMixin, View):
    template_name = "bulettin_board_app/app-edit-announce.html"

    def get(self, request, id):
        """
        The function displays announce to edit
        :param request:
        :param id:
        :return: render app-edit-announce.html
        """
        user = request.user
        annoucement = Announcement.objects.get(id=id)
        locations = Locations.objects.get(id=annoucement.locations_id)
        category = Category.objects.get(id=annoucement.category_id)
        try:
            photos = Photos.objects.get(announcement_id=id)
            ctx = {
                "annoucement": annoucement,
                "locations": locations,
                "photos": photos,
                "category": category,
                "user": user,
                "info": "Edycja ogłoszenia:"
            }
            return render(request, self.template_name, ctx)
        except Photos.DoesNotExist:
            ctx = {
                "annoucement": annoucement,
                "locations": locations,
                "category": category,
                "user": user,
            }
            return render(request, self.template_name, ctx)

    def post(self, request, id):
        """
        The function edit annouce
        :param request:
        :param id:
        :return: redirect detail_announce
        """
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
        locations.zipcode = request.POST.get("zipcode")
        locations.country = request.POST.get("country")

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


class SendEmailView(LoginRequiredMixin, View):

    def get(self, request, id):
        """

        :param request:
        :param id:
        :return:
        """
        annoucement = Announcement.objects.get(id=id)
        return render(request, 'bulettin_board_app/app-send-email.html', {'annoucement': annoucement})

    def post(self, request, id):
        """
        The function send email to the owner of the annouceme
        :param request:
        :param id:
        :return: redirect detalis_annouce
        """
        annoucement = Announcement.objects.get(id=id)
        email_sender = request.POST.get("email")
        topic = request.POST.get("topic")
        message = request.POST.get("desription")
        email_announce = "tomizdebski@gmail.com"
        send_mail(topic, message, email_sender, [email_announce], fail_silently=False)

        return redirect("details_announce", id=annoucement.id)


class ByCategoryView(View):

    def get(self, request, id_category):
        """
        The function display annoucements by category
        :param request:
        :param id_category:
        :return: render app-view-by-category.html
        """
        annoucements = Announcement.objects.filter(category_id=id_category)
        photos = Photos.objects.filter(announcement__in=annoucements)
        category = Category.objects.get(id=id_category)
        locations = Locations.objects.all()

        ctx = {
            "annoucements": annoucements,
            "photos": photos,
            "category": category,
            "locations": locations,
        }

        return render(request, "bulettin_board_app/app-view-by-category.html", ctx)


class SearchView(View):

    def get(self, request):
        return render(request, "bulettin_board_app/app-search.html")

    def post(self, request):
        """
        The function searches in names and descriptions
        :param request:
        :return: render app-search.html
        """
        search_query = request.POST.get('search')
        result = Announcement.objects.annotate(search=SearchVector('name', 'description'), ).filter(search=search_query)
        photos = Photos.objects.filter(announcement__in=result)
        ctx = {
            "search": search_query,
            "annoucements": result,
            "photos": photos,
        }
        return render(request, "bulettin_board_app/app-search.html", ctx)


class WatchingAnnounceView(LoginRequiredMixin, View):

    def get(self, request):
        """
        The functions displays an watching announce
        :param request:
        :return: render app-watching-announce.html
        """
        user = request.user
        watching = Watching.objects.filter(user_id=user.id)
        annoucements = Announcement.objects.filter(watching__in=watching)
        photos = Photos.objects.filter(announcement__in=annoucements)
        if not annoucements:
            info = "Nie obserwujesz jeszcze żadnych ogłoszeń"
        else:
            info = "Obserwowane"
        ctx = {
            "annoucements": annoucements,
            "photos": photos,
            "info": info,
        }
        return render(request, "bulettin_board_app/app-watching-announce.html", ctx)


class AddToWatchingView(LoginRequiredMixin, View):

    def get(self, request, id):
        """
        The functions add to watching announce
        :param request:
        :param id:
        :return: render app-watching-announce.html
        """
        user = request.user
        Watching.objects.create(
            user_id=user.id,
            announcement_id=id
        )

        return render(request, "bulettin_board_app/app-watching-announce.html")


class DeleteWatchingView(LoginRequiredMixin, View):

    def get(self, request, id):
        """
        The functions delete watching announce
        :param request:
        :param id:
        :return: render app-watching-announce.html
        """
        watching = Watching.objects.get(announcement_id=id)
        watching.delete()

        return redirect("watching")


