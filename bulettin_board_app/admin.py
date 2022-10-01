from django.contrib import admin
from .models import Announcement, Category, Locations, Preferences, Photos, Reactions

admin.site.register(Announcement)
admin.site.register(Category)
admin.site.register(Locations)
admin.site.register(Preferences)
admin.site.register(Photos)
admin.site.register(Reactions)