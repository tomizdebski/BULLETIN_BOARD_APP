from random import shuffle

from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from bulettin_board_app.models import Announcement, Photos, Category


class IndexHtmlView(View):
    def get(self, request):
        annoucements = Announcement.objects.all()
        photos = Photos.objects.first()

        ctx = {
            "annoucements": annoucements,
            "photos": photos
        }

        return render(request, "bulettin_board_app/index.html", ctx)


class AddAnnounceView(CreateView):
    model = Announcement
    fields = '__all__'
    template_name = 'bulettin_board_app/form.html'

