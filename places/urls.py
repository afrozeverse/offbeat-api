from django.urls import path
from . import views
from .views import list_all_places 

urlpatterns = [
    path('get-places/', views.get_place,name='getPlaces'),
    path('delete-place/<uuid:id>/', views.delete_place,name='deletePlace'),
    path('update-place/<uuid:id>/', views.update_place,name='updatePlace'),
    path('create-place/', views.create_place,name='createPlace'),
    path('', list_all_places, name='list-all-places'),
]