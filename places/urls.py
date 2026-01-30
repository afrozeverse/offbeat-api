from django.urls import path
from . import views

urlpatterns = [
    path('get-places/', views.get_place,name='getPlaces'),
    path('delete-place/<uuid:id>/', views.delete_place,name='deletePlace'),
    path('update-place/<uuid:id>/', views.update_place,name='updatePlace'),
    path('create-place/', views.create_place,name='createPlace'),
]