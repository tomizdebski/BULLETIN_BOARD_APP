from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.IndexView.as_view(), name="index"),
    path('category/<int:id_category>', views.ByCategoryView.as_view(), name="by_category_view"),
    path('add-announce/', views.AddAnnounceView.as_view(), name="add_announce"),
    path('details-announce/<int:id>', views.DetailAnnounceIdView.as_view(), name="details_announce"),
    path('my-announce/', views.MyAnnounceView.as_view(), name="my_announce"),
    path('delete/<int:id>', views.DeleteView.as_view(), name="delete"),
    path('edit/<int:id>', views.EditView.as_view(), name="edit"),
    path('send-email/<int:id>', views.SendEmailView.as_view(), name='send_email'),
    path('searching/', views.SearchView.as_view(), name='searching'),
    path('watching/', views.WatchingAnnounceView.as_view(), name='watching'),
    path('add-to-watching/<int:id>', views.AddToWatchingView.as_view(), name='add_to_watching'),
    path('delete-watching/<int:id>', views.DeleteWatchingView.as_view(), name='delete_watching'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


