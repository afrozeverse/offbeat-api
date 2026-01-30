from django.db import models
import uuid
from users import models as user_models
from places import models as place_models

class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐️ Poor'),
        (2, '⭐️⭐️ Fair'),
        (3, '⭐️⭐️⭐️ Good'),
        (4, '⭐️⭐️⭐️⭐️ Very Good'),
        (5, '⭐️⭐️⭐️⭐️⭐️ Excellent'),
    ]
    id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    user_id=models.ForeignKey(user_models.Customer, on_delete=models.CASCADE)
    place_id=models.ForeignKey(place_models.Place, on_delete=models.CASCADE, null=True, blank=True)
    rating=models.IntegerField(choices=RATING_CHOICES, default=3)
    title=models.CharField(max_length=100)
    comment=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    def __str__(self):
        return f"{self.title} ({self.rating}⭐)"