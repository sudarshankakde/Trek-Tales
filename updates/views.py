from datetime import date, datetime
import email
from http import client
from django.conf import settings
from django.shortcuts import render
from Trek_Tales.settings import *
from updates.models import *
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail
import random
import razorpay
import os
from django.template.loader import render_to_string
from django.template import Context
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import EmailMessage
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


def Invoice_pdf(data: dict):
    template = get_template('MailTempletes/invoice_pdf.html')
    html = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None


def sendMail(sub, email, html_message, data: dict, TripID):
    subject = sub
    emails = email
    mail = EmailMessage(
        subject, html_message, settings.EMAIL_HOST_USER,  emails)
    mail.content_subtype = "html"  # this is the crucial part
    try:
        mail.attach(f'Invoice_#{TripID}.pdf',
                    Invoice_pdf(data), 'application/pdf')
    except:
        pass
    try:
        mail.send(fail_silently=False)
        print("Mail Sent")
    except Exception as e:
        print(e)


def checkTourExpiry(tour):
    if (tour.tour_on_date >= date.today()):
        tour.TourIsNotExpire = True
        tour.save()
    else:
        tour.TourIsNotExpire = False
        tour.save()
    return


def update(request):
    reponse_data = Updates.objects.order_by('-tour_on_date').all()
    for i in reponse_data:
        checkTourExpiry(i)
    peginator = Paginator(reponse_data, 6)
    page_number = request.GET.get('page', 1)
    tours = peginator.get_page(page_number)
    if(request.htmx):
        return render(request, 'card.html', {'tours': tours})
    return render(request, 'tours/updates.html', {'tours': tours})


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
        return render(request, 'tours/Expired.html', {'slotsRemaing': slorts, 'updates': tour})
    else:
        return render(request, 'tours/BookSlot_form.html', {'slotsRemaing': slorts, 'updates': tour, "Razorpay_ApiKey": Razorpay_ApiKey})


def details(request, slug):
    tour = get_object_or_404(Updates, slug=slug)
    checkTourExpiry(tour)
    return render(request, 'tours/TourDetail.html', {'tour': tour})


def confirm_booking(request):
    id = request.POST.get('TourId')
    tour = get_object_or_404(Updates, id=id)
    slorts = tour.slorts
    if(request.method == 'POST'):
        fName = request.POST.get('fName')
        lName = request.POST.get('lastName')
        name = (f"{fName} {lName}").lower()
        email = request.POST.get('email')
        Phone_no1 = request.POST.get('Phone_no1')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        aadhaar = request.POST.get('aadhaar')
        birth_of_date = request.POST.get('birth_of_date')

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
            'sitedata': SiteData.objects.first(),
            'birth_of_date': birth_of_date,
            'aadhaar': aadhaar
        }
        return render(request, 'tours/paymentCard.html', context)

# def aadhaar_check(request):
#     if (request.method == 'GET'):
#         tour_id = request.GET.get('id')
#         aadhaar = request.GET.get('aadhaar')
#         instance = BookSlot.objects.filter(slotFor=tour_id)
#         print(instance)
#         if (instance.filter(aadhaar_number=aadhaar).exists()):
#             return HttpResponse("""<small id="AadhaarHelper" class="form-helper   opacity-70 my-1 w-75 text-danger"><i class="bi bi-info-circle-fill"></i> Booking have already been made using this Aadhaar</small>  <input type="hidden" value="false" id="aadhaar_Validate">""")
#         else:
#             return HttpResponse("""<small id="AadhaarHelper" class="form-helper   opacity-70 my-1 w-75 text-white"><i class="bi bi-info-circle-fill"></i> Aadhaar details are required for insurance purposes</small> <input type="hidden" value="true" id="aadhaar_Validate">""")


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
        aadhaar = request.POST.get('aadhaar')
        birth_of_date = request.POST.get('birth_of_date')
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
        print(birth_of_date)
        print(aadhaar)
        try:
            status = client.utility.verify_payment_signature(params_dict)
            if(razorpay_payment_id_exist == False & status):
                if tour.aadhaar_required:
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
                                    Payment_Status=Payment_Status,
                                    birth_of_date=birth_of_date,
                                    aadhaar_number=aadhaar)
                else:
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
                                    Payment_Status=Payment_Status,
                                    birth_of_date=birth_of_date,
                                    )
                slot.save()
                context_dist_recipt = {
                    "name": name,
                    "contactNumber": Phone_no1,
                    "company": {
                        "phone_no": SiteData.objects.first().SecondNumber,
                        "email": SiteData.objects.first().Email_id,
                        "phone_no2": SiteData.objects.first().WPNumber,
                        "bio_link": SiteData.objects.first().bio_link,
                    },
                    "tour_Name": tour.Heading,
                    "PaymentID": razorpay_payment_id,
                    "Date_Of_Payment": datetime.today(),
                    "tour": tour,
                    "charges_Amount": int(amount)-tour.price,
                    "totalPaid": amount,
                    "TripId": TripId}
                subject = f'Slot Booked Succesfully'
                html_message = render_to_string(
                    'MailTempletes/Payment_Recipt.html', context_dist_recipt)
                plain_message = strip_tags(html_message)
                Mail_To = [email, tour.Organizer.mail]
                sendMail(sub=subject,
                         email=Mail_To, html_message=html_message, data=context_dist_recipt, TripID=TripId)
                # 1 slort get reserved
                tour.slorts = tour.slorts - 1
                tour.save()
                return render(request, 'tours/PaymentSuccess.html', {'Payment_Status': Payment_Status, 'razorpay_payment_id': razorpay_payment_id, 'TripId': TripId, "Name": name, "amount": amount, 'tour': tour.Heading, 'state': 'success'})
            else:
                return render(request, 'tours/PaymentSuccess.html', {'state': "PaymentIdExist", 'Payment_Status': Payment_Status, 'razorpay_payment_id': razorpay_payment_id, 'TripId': TripId, "Name": name, "amount": amount, 'tour': tour.Heading, })
        except Exception as e:
            slot = BookSlot(Name=name, gender=gender, Phone_no1=Phone_no1,
                            address=address, amount=amount, slotFor=Updates(id=tourId), email=email, TripId=TripId, razorpay_signature=razorpay_signature, razorpay_order_id=razorpay_order_id, razorpay_payment_id=razorpay_payment_id,
                            Payment_Status=Payment_Status)
            slot.save()
            print(e)
            return render(request, 'tours/PaymentSuccess.html', {'issue': ' signature dont match', 'state': 'signatureNotMatch', })


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
            tansport_type = request.POST['tansport_type']
            # get founders mail id
            try:
                founder_tag_id = get_object_or_404(Tags, Tag='Founder')

                trip = customized_tour(
                    name=name,
                    email=email,
                    phone=phone,
                    group_size=group_size,
                    start_date=start_date,
                    no_of_day=no_of_day,
                    trek_name=trek_name,
                    tour_explain=tour_explain,
                    tansport_type=tansport_type
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
                    'tansport_type': tansport_type,
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
                send_mail(f"{name}  want customized tour", f"{name} had requested for customized tour here are details- {context}", mail_from, settings.MANAGERS,
                          fail_silently=True)
                return HttpResponse(f"""<div class="text-center my-4">Dear {request.POST['fName']}, Our executive will get back to you within a day, with a travel plan and other details as per your requested requirements.
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


def show_person_details(request, id):
    response = get_object_or_404(customized_tour, id=id)
    return render(request, 'admin/show_person_Details.html', {'data': response})
