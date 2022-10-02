from django.urls import path, include
from . import views
from .views import IndexHtmlView, AddAnnounceView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', IndexHtmlView.as_view(), name="index"),
    path('add-announce/', AddAnnounceView.as_view(), name="add_announce"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
