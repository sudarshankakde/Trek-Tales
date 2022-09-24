import datetime
import time
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
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
from Trek_Tales.settings import *
import updates
from updates.models import *
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django import forms
import random
import razorpay
import os
from twilio.rest import Client
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
global siteData
global linktree
siteData = SiteData.objects.first
linktree = 'https://linktr.ee/Treak_Tales'


def update(request):
    reponse_data = Updates.objects.order_by('-tour_on_date').all()
    peginator = Paginator(reponse_data, 6)
    page_number = request.GET.get('page', 1)
    tours = peginator.get_page(page_number)
    if(request.htmx):
        return render(request, 'card.html', {'tours': tours })
    return render(request, 'tours/updates.html', {'tours': tours })


Whatsapp = SiteData.objects.first().WP_Link
Instagram = SiteData.objects.first().Instagram_Profile_Link


def GenrateTripID(name, gender, tourId):
    randomNumber = random.randint(1500, 9999)
    TripId = f"{gender[0]}{randomNumber}{name.split()[1]}{tourId}"
    return TripId


def bookslot(request, slug):
    tour = get_object_or_404(Updates, slug=slug)
    tourId = tour.id
    slorts = tour.slorts
    
    if slorts < 1 or tour.TourIsNotExpire == False:
        return render(request, 'tours/Expired.html', {'slotsRemaing': slorts, 'updates': tour })
    else:
        return render(request, 'tours/BookSlot_form.html', {'slotsRemaing': slorts, 'updates': tour, "Razorpay_ApiKey": Razorpay_ApiKey})


def details(request, slug):
    tour = get_object_or_404(Updates, slug=slug)
    return render(request, 'tours/TourDetail.html', {'tour': tour })


def confirm_booking(request):
    id = request.POST.get('TourId')
    tour = get_object_or_404(Updates, id=id)
    slorts = tour.slorts
    if(request.method == 'POST'):
        fName = request.POST.get('fName')
        lName = request.POST.get('lastName')
        name = (f"{fName} {lName}")
        email = request.POST.get('email')
        Phone_no1 = request.POST.get('Phone_no1')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        def calculate_Payable_Amount(price):
            return (price+((price * Payment_Charges)/100))

        client = razorpay.Client(
            auth=(Razorpay_ApiKey, Razorpay_Api_SecretKey))
        payable_Amount = calculate_Payable_Amount(tour.price)
        payable_Amount = round(payable_Amount)
        data = {"amount": (payable_Amount * 100), "currency": "INR", "receipt": tour.Heading,
                'payment_capture': '1'}
        payment = client.order.create(data=data)
        payment_order_id = payment['id']
        context = {
            'name': name,
            'email': email,
            'gender': gender,
            'address': address,
            'Phone_no1': Phone_no1,
            'slotsRemaing': slorts,
            'updates': tour,
            'payable_Amount': payable_Amount,
            'Payment_charges': Payment_Charges,
            "Razorpay_ApiKey": Razorpay_ApiKey,
            'order_id': payment_order_id,
            'sitedata': siteData,
        }
        return render(request, 'tours/paymentCard.html', context)


def Payment_Completed(request):
    if request.method == 'POST':
        # featching data from frontend
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        Phone_no1 = request.POST.get('Phone_no1')
        # tour id
        tourId = request.POST.get('TourId')
        # payment details
        amount = request.POST.get('amount')
        Payment_Status = request.POST.get('Payment_Status')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        # uniqe trip id for each booking
        TripId = GenrateTripID(name, gender, tourId)
        client = razorpay.Client(
            auth=(Razorpay_ApiKey, Razorpay_Api_SecretKey))
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        razorpay_payment_id_exist = BookSlot.objects.filter(
            razorpay_payment_id=razorpay_payment_id).exists()

        # tour
        tour = get_object_or_404(Updates, id=tourId)

        try:
            status = client.utility.verify_payment_signature(params_dict)
            if(razorpay_payment_id_exist == False & status):
                slot = BookSlot(Name=name,
                                gender=gender,
                                Phone_no1=Phone_no1,
                                address=address,
                                amount=amount,
                                slotFor=Updates(id=tourId),
                                email=email,
                                TripId=TripId,
                                razorpay_signature=razorpay_signature,
                                razorpay_order_id=razorpay_order_id,
                                razorpay_payment_id=razorpay_payment_id,
                                Payment_Status=Payment_Status)
                slot.save()
                context_dist_recipt = {
                    "name": name,
                    "company": {
                        "phone_no": SiteData.objects.first().SecondNumber,
                        "email": SiteData.objects.first().Email_id
                    },
                    "tour_Name": tour.Heading,
                    "PaymentID": razorpay_payment_id,
                    "Date_Of_Payment": datetime.date.today(),
                    "tour": tour,
                    "charges_Amount": int(amount)-tour.price,
                    "totalPaid": amount,
                    'TripId': TripId}
                subject = f'Slot Booked Succesfully'
                html_message = render_to_string(
                    'MailTempletes/Payment_Recipt.html', context_dist_recipt)
                plain_message = strip_tags(html_message)
                Mail_From = settings.EMAIL_HOST_USER
                Mail_To = [email, tour.Organizer.mail]
                send_mail(subject, plain_message, Mail_From, Mail_To,
                          html_message=html_message, fail_silently=True)

                # 1 slort get reserved

                tour.slorts = tour.slorts - 1
                tour.save()

                return render(request, 'tours/PaymentSuccess.html', {'Payment_Status': Payment_Status, 'razorpay_payment_id': razorpay_payment_id, 'TripId': TripId, "Name": name, "amount": amount, 'tour': tour.Heading, 'state': 'success'})
            else:
                return render(request, 'tours/PaymentSuccess.html', {'state': "PaymentIdExist", 'Payment_Status': Payment_Status, 'razorpay_payment_id': razorpay_payment_id, 'TripId': TripId, "Name": name, "amount": amount, 'tour': tour.Heading , })
        except:
            slot = BookSlot(Name=name, gender=gender, Phone_no1=Phone_no1,
                            address=address, amount=amount, slotFor=Updates(id=tourId), email=email, TripId=TripId, razorpay_signature=razorpay_signature, razorpay_order_id=razorpay_order_id, razorpay_payment_id=razorpay_payment_id,
                            Payment_Status=Payment_Status)
            slot.save()
            return render(request, 'tours/PaymentSuccess.html', {'issue': ' signature dont match', 'state': 'signatureNotMatch' , })


def Payment_Failed(request):
    return render(request, 'tours/Payment_fail.html')


def customize_tour(request):
    if request.user.is_authenticated:
        data = customized_tour.objects.order_by('-request_on_date').all()
        if(request.method == "POST"):
            if 'filter_month' in request.POST:
                filter_month = request.POST['filter_month']
            else:
                filter_month = datetime.now().month
            seprated_data = filter_month.split('-')
            month = seprated_data[1]
            year = seprated_data[0]
            filter_data = customized_tour.objects.filter(
                request_on_date__month=month,
                request_on_date__year=year).order_by('-request_on_date__time')
            print(filter_data)
            return render(request, 'customize_tour/table.html', {"data": filter_data})
        return render(request, 'customize_tour/customize_tour.html', {'data': data, })
    else:
        if(request.method == 'POST'):
            name = request.POST['fName'] + " " + request.POST['lastName']
            email = request.POST['email']
            phone = request.POST['phone']
            group_size = request.POST['group_size']
            start_date = request.POST['start_date']
            no_of_day = request.POST['no_of_day']
            trek_name = request.POST['trek_name']
            tour_explain = request.POST['tour_explain']
            # get founders mail id
            try:
                founder_tag_id = get_object_or_404(Tags, Tag='Founder')
                founders = Organizer.objects.filter(Tags=founder_tag_id).all()
                foundersMail = []
                for founder in founders:
                    foundersMail.append(founder.mail)
                trip = customized_tour(
                    name=name,
                    email=email,
                    phone=phone,
                    group_size=group_size,
                    start_date=start_date,
                    no_of_day=no_of_day,
                    trek_name=trek_name,
                    tour_explain=tour_explain
                )
                context = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "group_size": group_size,
                    "start_date": start_date,
                    "no_of_day": no_of_day,
                    "trek_name": trek_name,
                    "tour_explain": tour_explain,
                    'sitedata': SiteData.objects.first(),
                }
                trip.save()
                subject = f"""personalized tour requirements saved"""
                mail_from = settings.EMAIL_HOST_USER
                html_message = render_to_string(
                    'MailTempletes/customize_tour.html', context)
                plain_message = strip_tags(html_message)
                # mail to user
                send_mail(subject, plain_message, mail_from, [email],
                          html_message=html_message, fail_silently=True)

                # mail to founders
                send_mail(f"{name}  want customized tour", f"{name} had requested for customized tour here are details- {context}", mail_from, foundersMail,
                          fail_silently=True)

                return HttpResponse("""<div class="text-center my-4">We will get back to you within a day, with a travel plan and other details as per your requested requirements.
                <br>
                <br>
                    <a href="../tours/" class=" mt-4 text-decoration-underline opacity-80 text-user-primary">
                            See Upcoming Tour
                    </a>
                </div>
                """)
            except Exception as e:
                return HttpResponse('some error '+str(e))
    return render(request, 'customize_tour/customize_tour.html')
