from email import message
from pyexpat import model
from django.db import models
from django.forms import CharField

# Create your models here.


class Updates(models.Model):
    Tour_image = models.ImageField(upload_to='media/tour',verbose_name="tour image shown on cards.")
    Tumbnail  = models.ImageField(upload_to='media/tour/tubnail',verbose_name="detailed thubnail")
    Heading = models.CharField(max_length=100,verbose_name="heading text")
    location = models.CharField(max_length=100)
    price = models.IntegerField(verbose_name="price Of tour")
    tour_on_date = models.DateField(auto_now=False)
    slorts = models.IntegerField()
    packageInfo = models.TextField()
    Tour_added = models.DateTimeField(auto_now=True, editable=False, auto_created=True)
    TourIsNotExpire = models.BooleanField(default=False)
    def __str__(self):
        return (f"{self.location} | {self.tour_on_date}")


class Testimonials(models.Model):
    ReviewBy = models.CharField(max_length=25,verbose_name="review given by")
    Review = models.TextField(verbose_name="what is Review")
    ReviewerImage = models.ImageField(upload_to='media/Testimonials',verbose_name="reviewer's image")
    profession = models.CharField(max_length=25,verbose_name="Profession Of reviewer")
    date_added = models.DateTimeField(auto_now=True,editable=False,auto_created=True)
    def __str__(self):
        return (f"{self.ReviewBy}")


class BookSlot(models.Model):
    slotFor = models.ForeignKey(Updates(id),on_delete=models.CASCADE,blank=True)
    Name = models.CharField(max_length=30)
    gender = models.CharField(max_length=7)
    TripId = models.CharField(max_length=20)
    email = models.EmailField(blank=True,null=True,default='null@gmail.com')
    Phone_no1 = models.IntegerField()
    address = models.TextField()
    amount = models.IntegerField(default=0)
    def __str__(self):
        return (f"{self.TripId} || {self.slotFor} || {self.Name} | {self.Phone_no1}")


class SiteData(models.Model):
    WPNumber = models.IntegerField()
    SecondNumber = models.IntegerField()
    Instagram_Profile_Link = models.URLField(max_length=200)
    WP_Link = models.URLField(max_length=200)
    Email_id = models.EmailField(max_length=254)
    def __str__(self):
        return self.Email_id


class Contact(models.Model):
    FullName = models.CharField(max_length=30)
    Message = models.TextField()
    Email = models.EmailField()
    Contact_on = models.DateField(auto_created=True,auto_now=True)

    def __str__(self) :
        return f"{self.FullName} | {self.Contact_on}"


