from django.db import models
from updates.models import Updates
from django_resized import ResizedImageField
# Create your models here.


class Memories(models.Model):
    photo_taken_on_tour = models.ForeignKey(Updates(id), on_delete=models.PROTECT,default="unknown tour", null=True)
    photos_taken = models.ImageField(upload_to="Gallary/Images", max_length=None)
    author = models.CharField(max_length=50,verbose_name="name or insta username of person who had taken this pic",default='kiran J',null=True)
    def __str__(self):
        return (f"{self.photo_taken_on_tour} | {self.author}")
