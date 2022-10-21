from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)

    # def get_absolute_url(self):
    #     return reverse("update_category", args=(self.id,))

    def __str__(self):
        return f"{self.name} "


class Locations(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    province = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("map", args=(self.id,))

    def __str__(self):
        return f"{self.name} "


class Announcement(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    locations = models.ForeignKey(Locations, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("details-announce", args=(self.id,))

    def __str__(self):
        return f"{self.name} "


REACTIONS = (
    (1, "like"),
    (2, "dislike"),
    (3, "love")
)


class Reactions(models.Model):  # reactions
    like = models.IntegerField(choices=REACTIONS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)


class Preferences(models.Model):
    # name = models.CharField(max_lenght=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    locations = models.ForeignKey(Locations, on_delete=models.CASCADE)


class Photos(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    img = models.ImageField(upload_to="images/")
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)


class Watching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
