from django.urls import path
from . import views
urlpatterns = [
    path('my-places/',views.placesView),
    path('my-place-details/<uuid:pk>/',views.placeDetailView),
    path('my-services/',views.servicesView),
    path('my-service-details/<uuid:pk>/',views.serviceDetailView),
    path('my-reviews/',views.getReviews)
]
