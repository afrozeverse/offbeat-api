from django.db import models
import uuid
from users import models as user_models
from places import models as places_models


class Service(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    provider=models.ForeignKey(user_models.Provider, on_delete=models.CASCADE)
    place=models.ForeignKey(places_models.Place, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    service_type = models.CharField(max_length=50)
    price_from=models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    price_to=models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    languages=models.JSONField(default=list, blank=True)  # list of languages offered
    capacity=models.IntegerField(null=True,blank=True)
    availability = models.TextField(blank=True, null=True)  # text or structured data
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    contact_method = models.CharField(
        max_length=20,
        choices=[
            ('phone', 'Phone'),
            ('message', 'Message'),
            ('booking_link', 'Booking Link'),
        ],
        default='phone'
    )
    contact_detail=models.CharField(max_length=100,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.title