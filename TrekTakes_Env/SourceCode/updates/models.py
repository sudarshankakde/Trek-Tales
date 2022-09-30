from email import message
from pyexpat import model
from django.db import models
from django.forms import CharField
from django_resized import ResizedImageField
from autoslug import AutoSlugField
import uuid
# Create your models here


class Tags(models.Model):
    Tag = models.CharField(max_length=50)
    def __str__(self):
        return self.Tag


class Organizer(models.Model):
    Name = models.CharField(max_length=50)
    Tags = models.ManyToManyField(Tags(id), verbose_name=("Tags"))
    About = models.CharField(max_length=250)
    whatsapp = models.URLField(max_length=200)
    instagram = models.URLField(max_length=200)
    telephone = models.IntegerField()
    mail = models.EmailField(max_length=254)
    image = models.ImageField(upload_to='tours/Images/organizers')
    backgroundImg = ResizedImageField(size=[800, 450], quality=100, keep_meta=False,
                                      upload_to='tours/Images/organizers/bg', verbose_name="Background Image")

    def __str__(self):
        return f"{self.Name}"


class Updates(models.Model):
    Tour_image = ResizedImageField(size=[375, 225], crop=[
                                   'middle', 'center'], quality=100, keep_meta=False, upload_to='tours/Images/tour', verbose_name="tour image shown on cards.")
    Tumbnail = ResizedImageField(size=[800, 450], quality=100, keep_meta=False,
                                 upload_to='tours/Images/tour/tubnail', verbose_name="detailed thubnail")
    Heading = models.CharField(max_length=50, verbose_name="heading text")
    slug = AutoSlugField(populate_from='Heading')
    location = models.CharField(max_length=100)
    price = models.IntegerField(verbose_name="price Of tour")
    tour_on_date = models.DateField(
        auto_now=False, verbose_name="Booking End on")
    tour_from_to = models.CharField(
        max_length=50, verbose_name="Date of Tour: month Form_date - To_date")
    time = models.TimeField(
        auto_now=False, auto_now_add=False, verbose_name="Tour will start on : Time")
    city = models.CharField(max_length=50, verbose_name="City Name of VENUE")
    district = models.CharField(
        max_length=50, verbose_name="District Name of VENUE")
    slorts = models.IntegerField()
    packageInfo = models.TextField()
    Tour_added = models.DateTimeField(
        auto_now=True, editable=False, auto_created=True)
    TourIsNotExpire = models.BooleanField(default=True,editable=False)
    Organizer = models.ForeignKey(Organizer(id), on_delete=models.PROTECT,default="1")
    googleMap = models.URLField(
        max_length=200, verbose_name="Google Map VENUE Url")

    def __str__(self):
        return (f"{self.location} | {self.Heading}")


class Testimonials(models.Model):
    ReviewBy = models.CharField(max_length=25, verbose_name="review given by")
    Review = models.TextField(verbose_name="what is Review")
    ReviewerImage = models.ImageField(
        upload_to='Images/Testimonials', verbose_name="reviewer's image")
    profession = models.CharField(
        max_length=25, verbose_name="Profession Of reviewer")
    date_added = models.DateTimeField(
        auto_now=True, editable=False, auto_created=True)

    def __str__(self):
        return (f"{self.ReviewBy}")


class BookSlot(models.Model):
    slotFor = models.ForeignKey(
        Updates(id), on_delete=models.PROTECT, blank=True,editable=False)
    Name = models.CharField(max_length=30)
    gender = models.CharField(max_length=7)
    TripId = models.CharField(unique=True, max_length=20, editable=False)
    email = models.EmailField(blank=True, null=True, default='null@gmail.com')
    Phone_no1 = models.IntegerField()
    address = models.TextField()
    amount = models.IntegerField(default=0,editable=False)
    razorpay_payment_id = models.CharField(
        unique=True, max_length=50, editable=False, null=True)
    razorpay_order_id = models.CharField(
        max_length=50, editable=False, null=True)
    razorpay_signature = models.CharField(
        max_length=50, editable=False, null=True)
    Payment_Status = models.BooleanField(default=False)


    def __str__(self):
        return (f"{self.TripId} || {self.slotFor} || {self.Name} | {self.Phone_no1}")


class SiteData(models.Model):
    WPNumber = models.IntegerField()
    SecondNumber = models.IntegerField()
    Instagram_Profile_Link = models.URLField(max_length=200)
    WP_Link = models.URLField(max_length=200)
    Email_id = models.EmailField(max_length=254)
    logo = models.ImageField(upload_to='siteData/logo',null=True)
    bio_link = models.URLField(max_length=200,null=True)

    def __str__(self):
        return self.Email_id


class Contact(models.Model):
    FullName = models.CharField(max_length=30)
    Message = models.TextField()
    Email = models.EmailField()
    Contact_on = models.DateField(auto_created=True, auto_now=True)

    def __str__(self):
        return f"{self.FullName} | {self.Contact_on}"


class NewsLetter_Subscriber(models.Model):
    Email_Id = models.EmailField(max_length=254)
    Subscribed_on = models.DateField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.Email_Id


class ReFund(models.Model):
    ReFund_For = models.ForeignKey(
        Updates(id), on_delete=models.CASCADE, blank=True)
    Name = models.CharField(max_length=30)
    gender = models.CharField(max_length=7)
    TripId = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True, default='null@gmail.com')
    Phone_no1 = models.IntegerField()
    address = models.TextField()
    amount = models.IntegerField(default=0)
    refund_Amount = models.IntegerField(default=0)
    cancelation_date = models.DateTimeField(auto_created=True, auto_now=True)
    charge_Day = models.IntegerField()
    charge_percenrate = models.IntegerField()
    razorpay_payment_id = models.CharField(
        max_length=50, editable=False, null=True)
    razorpay_order_id = models.CharField(
        max_length=50, editable=False, null=True)
    razorpay_signature = models.CharField(
        max_length=50, editable=False, null=True)
    Payment_Status = models.BooleanField(default=False)
    # true == Refunded , False == Yet to Refund
    Refund_Status = models.BooleanField(default=False)
    Refund_On = models.DateField(null='true')
    cancelation_Reason = models.CharField(max_length=50,null=True,default='no reason where mentioned , default value saved')

    def __str__(self):
        return f"{self.Name}|Rs.{self.refund_Amount}"


class customized_tour(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    group_size = models.IntegerField()
    no_of_day = models.IntegerField()
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    trek_name = models.CharField(max_length=50)
    tour_explain = models.TextField(null=True)
    request_on_date = models.DateTimeField(auto_created=True, auto_now=True)


