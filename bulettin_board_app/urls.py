from django.urls import path, include
from . import views
from .views import IndexView, new_annoucement, AddAnnounceViewTest
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', IndexView.as_view(), name="index"),
    path('add-announce/', AddAnnounceViewTest.as_view(), name="add_announce"),
    path('add/', views.new_annoucement, name="add"), #test forms
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
