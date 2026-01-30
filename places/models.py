from django.db import models
import uuid
from users import models as user_models
from django.utils import timezone

class Place(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title=models.CharField(max_length=200,null=True,blank=True)
    short_description=models.CharField(max_length=500,null=True,blank=True)            
    long_description=models.TextField()
    tags = models.JSONField(default=list, blank=True)
    coords = models.JSONField(default=dict, blank=True)
    address=models.TextField()
    state=models.CharField(max_length=100,null=True, blank=True)
    district=models.CharField(max_length=100,null=True, blank=True)
    image1 = models.ImageField(upload_to='places/', null=True, blank=True)
    image2 = models.ImageField(upload_to='places/', null=True, blank=True)
    image3 = models.ImageField(upload_to='places/', null=True, blank=True)
    image4 = models.ImageField(upload_to='places/', null=True, blank=True)
    accessibility_notes=models.TextField(blank=True,null=True) #Information on accessibility (e.g., wheelchair access).
    permits_info=models.TextField() #Notes about required permissions or passes.
    entry_fee=models.CharField( max_length=50)
    nearest_bus_stop=models.CharField(max_length=200,blank=True,null=True)
    nearest_railway_station=models.CharField(max_length=200,blank=True,null=True)
    nearest_airport=models.CharField(max_length=200,blank=True,null=True)
    suggested_duration=models.CharField(max_length=50,blank=True,null=True) #Recommended time to spend there.
    food=models.CharField(max_length=100,blank=True,null=True)
    accomodation=models.CharField(max_length=100,blank=True,null=True)
    overnight_stay=models.CharField(max_length=10,blank=True,null=True) #answer yes or no
    created_by=models.ForeignKey(user_models.Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class SuggestedEdit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    id=models.UUIDField(primary_key=True ,default=uuid.uuid4, editable=False)
    place_id=models.ForeignKey(Place, on_delete=models.CASCADE,related_name='suggested_edits')
    suggested_by=models.ForeignKey(user_models.Customer, on_delete=models.CASCADE, related_name='suggested_edits')
    payload = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id