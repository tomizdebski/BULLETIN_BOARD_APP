from random import shuffle

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from bulettin_board_app.forms import AnnoucementForm
from bulettin_board_app.models import Announcement, Photos, Category, Locations


class IndexView(View):
    def get(self, request):
        annoucements = Announcement.objects.all()
        photos = Photos.objects.first()

        ctx = {
            "annoucements": annoucements,
            "photos": photos
        }

        return render(request, "bulettin_board_app/index.html", ctx)


class AddAnnounceViewTest(View):
    def get(self, request):
        return render(request, "bulettin_board_app/app-add-annouce.html")

    def post(self, request):

        name = request.POST.get("name")
        description = request.POST.get('description')
        user = User.objects.get(is_staff=True)
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
def new_annoucement(request):
    if request.method != 'POST':
        form = AnnoucementForm()
    else:
        form = AnnoucementForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'bulettin_board_app/app-add-annouce.html', context)



