from django.urls import path
from . import views

urlpatterns = [
    path('get-reviews/<uuid:place_id>', views.get_reviews,name='getReviews'),
    path('create-review/', views.create_review,name='createReview'),
    path('delete-review/<uuid:id>', views.delete_review,name='deleteReview'),
    path('update-review/<uuid:id>', views.update_review,name='updateReview'),
]