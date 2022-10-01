from random import shuffle

from django.shortcuts import render
from django.views import View

from bulettin_board_app.models import Announcement, Photos


class IndexHtmlView(View):
    def get(self, request):
        annoucements = Announcement.objects.all()
        photos = Photos.objects.first()


        ctx = {
            "annoucements": annoucements,
            "photos": photos
        }

        return render(request, "bulettin_board_app/index.html", ctx)
