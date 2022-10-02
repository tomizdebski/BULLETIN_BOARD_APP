from django.urls import path, include
from . import views
from .views import IndexHtmlView, AddAnnounceView

urlpatterns = [

    path('', IndexHtmlView.as_view(), name="index"),
    path('add-announce/', AddAnnounceView.as_view(), name="add_announce"),


]
