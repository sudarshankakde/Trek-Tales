from django.db import models
from updates.models import Updates

# Create your models here.


class Memories(models.Model):
    photo_taken_on_date = models.DateField(
        auto_now=False, editable=True, null=True, blank=True, verbose_name="photo taken on ")
    # photo_taken_on_tour = models.ForeignKey("Updates", on_delete=models.CASCADE)
    photo_taken_on_tour = models.CharField(max_length=100)
    likes = models.IntegerField(editable=None, default=0, null=True)
    photos_taken = models.ImageField(
        upload_to="media/Gallary", height_field=None, width_field=None, max_length=None)
    photo_taken_on_location_url = models.URLField(max_length=200,verbose_name="google map location url")
    def __str__(self):
        return (f"{self.photo_taken_on_tour} | {self.photo_taken_on_date}")
