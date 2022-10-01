from django.urls import path, include
from . import views
from .views import IndexHtmlView

urlpatterns = [

    path('', IndexHtmlView.as_view(), name="index"),

]
