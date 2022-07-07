from ast import If
from datetime import date, datetime
import email
from http import client
from logging import warning
from multiprocessing.connection import Client
from multiprocessing.sharedctypes import Value
from optparse import Values
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from Trek_Tales.settings import Razorpay_Api_SecretKey, Razorpay_ApiKey, Twilio_SID, Twilio_Token
import updates
from updates.models import Updates, Testimonials, BookSlot, SiteData
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import pyshorteners
from django.core.mail import send_mail
from django import forms
from captcha.fields import ReCaptchaField
import random
import razorpay
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = Twilio_SID
auth_token = Twilio_Token
clientWp = Client(account_sid, auth_token)


client = razorpay.Client(auth=(Razorpay_ApiKey, Razorpay_Api_SecretKey))

global linktree
linktree = 'https://linktr.ee/Treak_Tales'


def update(request):
    tours = Updates.objects.order_by('-tour_on_date')[0:4]
    for tour in tours:
        tourOnDate = tour.tour_on_date
        if tourOnDate < date.today():
            tour.TourIsNotExpire = False
            tour.save()
        else:
            tour.TourIsNotExpire = True
            tour.save()
    return render(request, 'updates.html', {'tours': tours})


shortlink = pyshorteners.Shortener()
Whatsapp = shortlink.tinyurl.short(SiteData.objects.first().WP_Link)
Instagram = shortlink.tinyurl.short(
    SiteData.objects.first().Instagram_Profile_Link)


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()


def GenrateTripID(lName, gender, tourId):
    randomNumber = random.randint(1500, 9999)
    TripId = f"{gender[0]}-{randomNumber}-{lName}-{tourId}"
    return TripId


def bookslot(request, id):
    tour = get_object_or_404(Updates, id=id)
    tourId = id
    slorts = tour.slorts
    sitedata = SiteData.objects.first()
    warningRecaptcha = "Fill CAPTHA To Proceed"

    client = razorpay.Client(auth=(Razorpay_ApiKey, Razorpay_Api_SecretKey))
    data = {"amount": tour.price*100, "currency": "INR"}
    payment = client.order.create(data=data)
    payment_id = payment['id']
    if request.method == "POST":
        fName = request.POST.get('fName')
        lName = request.POST.get('lastName')
        name = (f"{fName} {lName}")
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        Phone_no1 = request.POST.get('Phone_no1')
        address = request.POST.get('address')
        amount = request.POST.get('amount')
        if tour.slorts > 0:
            TripId = GenrateTripID(lName, gender, tourId)
            slot = BookSlot(Name=name, gender=gender, Phone_no1=Phone_no1,
                            address=address, amount=amount, slotFor=Updates(id=tourId), email=email, TripId=TripId)
            slot.save()
            messages.success(
                request, f'Awesome <i class="bi bi-emoji-laughing"></i>,Slot Booked Successfully .Check Email For All Details')

            # send email
            Mail_Subject = f'Slot Booked Succesfully'
            Mail_Message = f"Hello {name}, I am glad to inform you that your booking for {tour.Heading} the amount Rs.{tour.price} has been completed successfully your Trip ID is {TripId} .Please stay in touch with us for updates. {linktree}"
            Mail_To = [email, ]
            Mail_From = settings.EMAIL_HOST_USER
            send_mail(Mail_Subject, Mail_Message, Mail_From,
                      Mail_To, fail_silently=True)

            # 1 slort get reserved
            tour.slorts = tour.slorts - 1
            tour.save()
            

            message = clientWp.messages.create(
                from_='whatsapp:'+ settings.TWILIO_NUMBER,
                body=f'Slot Booked By {name} for Trip of {tour.location} And payment Method is Cash on Pay Payable Amount will be {amount}. Contact Details Are: 1. Mobile Number +91{Phone_no1} 2.Gmail Id {email} 3.Address {address} 4.TripId {TripId} contact on wp to notify them https://api.whatsapp.com/send?phone=+91{Phone_no1}&text=Hello%20{fName}%20{lName}%20your%20Slot%20is%20booked%20successfully.%20Thanks%20For%20Choosing%20Us!',
                to='whatsapp:+919021767520'
            )
    return render(request, 'bookSlot.html', {'slotsRemaing': slorts, 'updates': tour})


def getMoreUpdates(request, number):
    alreadyAvalable = int(number)
    toSend = alreadyAvalable+4
    tours = Updates.objects.order_by('-tour_on_date')[alreadyAvalable:toSend]
    for tour in tours:
        tourOnDate = tour.tour_on_date
        if tourOnDate < date.today():
            tour.TourIsNotExpire = False
            tour.save()
        else:
            tour.TourIsNotExpire = True
            tour.save()

    return JsonResponse({"data": list(tours.values())})
