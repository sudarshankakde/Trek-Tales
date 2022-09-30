from django.utils.html import strip_tags
from django.template.loader import render_to_string
import email
from unicodedata import name
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from updates.models import *
from Gallary.models import Memories
from datetime import date, timedelta
from django.contrib import messages
from django_pandas.io import read_frame
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from Trek_Tales.settings import *
from django.core.files.storage import FileSystemStorage
import datetime
import xlwt
from updates.views import checkTourExpiry
# Create your views here.


@login_required
def admin_links(request):

    return render(request, 'admin_links.html')


def home(request):
    gallary = Memories.objects.order_by('-photo_taken_on_tour')[0:5]
    updates = Updates.objects.order_by('-tour_on_date')[0:3]
    for i in updates:
        checkTourExpiry(i)
    testimonials = Testimonials.objects.order_by('-date_added')[:6]
    return render(request, 'home.html', {'tours': updates, 'Testimonials': testimonials, 'gallary': gallary})


def contact(request):
    if request.method == 'POST':
        MailId = request.POST.get('email')
        Message = request.POST.get('message')
        Name = request.POST.get('name')
        contact = Contact(FullName=Name, Message=Message, Email=MailId)
        contact.save()

        # mail main content
        Main_content = f"""Dear {Name}, we have received your
        comment/suggestion. A member of our team will
        contact you shortly. Thank you for visiting
        Trek.Tales"""

        subject = f'We Will Reach To You soon'
        html_message = render_to_string(
            'MailTempletes/Contact-Cancelation_mail_templete.html', {'Main_content': Main_content})
        plain_message = strip_tags(html_message)
        Mail_From = settings.EMAIL_HOST_USER
        Mail_To = [MailId, ]
        send_mail(subject, plain_message, Mail_From, Mail_To,
                  html_message=html_message, fail_silently=True)
        return HttpResponse(f"""Your response is saved. A member of our team will
        contact you shortly!""")

    return render(request, 'contact.html', )


def cancelation(request):
    if request.method == 'POST':
        TripId = request.POST.get('TripId')
        cancelation_Reason = request.POST.get('cancelation_Reason')
        TripId = TripId.replace(" ", "")

        def calculate_RefundAmout(charges, price):
            return (price-((price * charges)/100))
        try:
            instance = get_object_or_404(BookSlot, TripId=TripId)
            if(instance.slotFor.tour_on_date < datetime.date.today()):
                return HttpResponse("""tour is already expired.""")
            else:
                Organizer_mail = instance.slotFor.Organizer.mail
                tourId = instance.slotFor.id
                tour = get_object_or_404(Updates, id=tourId)
                tour.slorts = tour.slorts + 1
                tour_price = instance.slotFor.price
                cancelation_charge_days = (
                    instance.slotFor.tour_on_date - datetime.date.today()).days
                # charge calculations

                if(cancelation_charge_days >= 25):
                    charges = Refund_Charges['More_Then_25_Days_Remain']
                    RefundAmout = calculate_RefundAmout(charges, tour_price)
                elif(cancelation_charge_days >= 15 & cancelation_charge_days < 25):
                    charges = Refund_Charges['More_Then_15_Days_Remain']
                    RefundAmout = calculate_RefundAmout(charges, tour_price)
                elif(cancelation_charge_days < 15):
                    charges = Refund_Charges['Less_Then_15_Days_Remain']
                    RefundAmout = calculate_RefundAmout(charges, tour_price)
                # refund Amount

                # mail main content
                if(instance.Payment_Status):
                    Main_content = f"""Please be Informed that we have canceled your trip to {tour.Heading} with <br> Trip Id:( {TripId} ) and<br> Payment ID :( {instance.razorpay_payment_id} ) <br> Thanks , {instance.Name}. you will get refund of Rs.{RefundAmout} ({charges}% charges on Rs.{tour_price}) within 48-72 hours. <br>For instant Refund you can Send your UPI Id or Back Account Details on {instance.slotFor.Organizer.telephone} among With your payment id and Trip ID.
                    <br><br>Cancelation Done {cancelation_charge_days} Days Before Tour Date"""
                    # subject
                    subject = f'Regarding cancelation Of Tour.'
                    html_message = render_to_string(
                        'MailTempletes/Contact-Cancelation_mail_templete.html', {'Main_content': Main_content})
                    plain_message = strip_tags(html_message)
                    Mail_From = settings.EMAIL_HOST_USER
                    Mail_To = [instance.email]
                    # mail sent
                    send_mail(subject, plain_message, Mail_From, Mail_To,
                              html_message=html_message, fail_silently=True)

                    # mail to Organizer
                    subject = f"{instance.Name} Cancel The Trip"
                    Main_content = f"""
                    Name: {instance.Name}. <br> 
                    Payment ID :  {instance.razorpay_payment_id} <br>
                    Trip Id: {TripId}<br>
                    Refund Amount: {RefundAmout} ({charges}% charges on Rs.{tour_price}) [{cancelation_charge_days} Days Before Cancelation] <br>
                    Email: {instance.email} <br>
                    Phone no: {instance.Phone_no1} <br>
                    razorpay_order_id : {instance.razorpay_order_id} <br>
                    Tour Detail : {instance.slotFor.Heading}|{instance.slotFor.location} <br>
                    <br><br>Cancelation Done {cancelation_charge_days} Days Before Tour Date"""
                    html_message = render_to_string(
                        'MailTempletes/Contact-Cancelation_mail_templete.html', {'Main_content': Main_content})
                    Mail_To = [Organizer_mail]
                    # mail sent
                    send_mail(subject, plain_message, Mail_From, Mail_To,
                              html_message=html_message, fail_silently=True)

                    refund = ReFund(Name=instance.Name, ReFund_For=instance.slotFor, gender=instance.gender, TripId=instance.TripId, email=instance.email, Phone_no1=instance.Phone_no1, address=instance.address, amount=instance.amount, razorpay_payment_id=instance.razorpay_payment_id,
                                    razorpay_order_id=instance.razorpay_order_id, razorpay_signature=instance.razorpay_signature, Payment_Status=instance.Payment_Status, refund_Amount=RefundAmout, charge_Day=cancelation_charge_days, charge_percenrate=charges, cancelation_Reason=cancelation_Reason)
                    refund.save()
                    instance.slotFor.slorts += 1
                    instance.slotFor.save()
                    instance.delete()
                    tour.save()
                    return HttpResponse('Cancelation Done 🪂')
                else:
                    instance = get_object_or_404(BookSlot, TripId=f"{TripId}")
                    Organizer_mail = instance.slotFor.Organizer.mail
                    tourId = TripId[-1]
                    tour = get_object_or_404(Updates, id=tourId)
                    tour.slorts = tour.slorts + 1
                    tour_price = instance.slotFor.price
                    instance.slotFor.slorts += 1
                    instance.slotFor.save()
                    instance.delete()
                    tour.save()
                    return HttpResponse('Cancelation Done 🪂 | No Refund For Your Booking Were Found!')
        except Exception as e:
            if request.user.is_authenticated:
                return HttpResponse(f"""Cancelation Failed Please Enter Valid Trip ID<br>{e}""")
            else:
                return HttpResponse('Cancelation Failed Please Enter Valid Trip ID')

    return render(request, 'tours/cancelation.html')


def aboutUs(request):
    total_Tours = 256
    total_Costumers = 900
    total_Review = 300
    Founders = Organizer.objects.filter(
        Tags=Tags.objects.get(Tag='Founder').id)
    organizer = Organizer.objects.order_by('-id')
    return render(request, 'aboutUs.html', {'total_Tours': total_Tours, 'total_Costumers': total_Costumers, 'total_Review': total_Review, 'Founders': Founders, 'organizer': organizer})


def error_404_view(request, exception):
    return render(request, '404.html',)


def error_500_view(request, *args, **kwargs):
    context_instance = RequestContext(request)
    return render(request, '404.html', )


@login_required
def ShowBookings(request):
    tours = Updates.objects.order_by('-tour_on_date')
    return render(request, 'tours/ShowBookings.html', {'tours': tours})


@login_required
def ShowBookingsOfId(request, id):
    tours = Updates.objects.order_by('-tour_on_date')
    BookedSlots = BookSlot.objects.filter(slotFor=id).order_by('-id')
    refund = ReFund.objects.filter(ReFund_For=id).order_by('-cancelation_date')
    BookedSlotsHeading = Updates.objects.filter(id=id).first()

    def calculate_Payable_Amount(price):
        return (price+((price * Payment_Charges)/100))
    payable_Amount = calculate_Payable_Amount(BookedSlotsHeading.price)
    payable_Amount = round(payable_Amount)
    platfrom_fee = int(payable_Amount)-int(BookedSlotsHeading.price)

    return render(request, 'tours/ShowBookings.html', {'BookedSlots': BookedSlots, 'tours': tours, 'BookedSlotsHeading': BookedSlotsHeading, 'ReFund': refund, 'payable_Amount': payable_Amount, 'Payment_Charges': Payment_Charges, 'platfrom_fee': platfrom_fee})


@login_required
def exportExcel(request, id):
    try:
        if(BookSlot.objects.filter(slotFor=id).count() < 1):
            return HttpResponse('No enterys for this tour yet')
        else:
            rows = BookSlot.objects.filter(slotFor=id).values_list(
                'Name', 'gender', 'Phone_no1', 'email', 'address', 'TripId', 'razorpay_payment_id', 'Payment_Status', 'razorpay_order_id')
            tourIs = Updates.objects.filter(id=id).first()
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition '] = f'attachment;filename={tourIs.Heading}|Rs.{tourIs.price}|DowloadedOn__' +\
                str(datetime.datetime.now())+".xls"
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('BookedSlots')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['Name', 'gender', 'Phone_no1',
                       'email', 'address', 'TripId', 'razorpay_payment_id', 'Payment_Status', 'razorpay_order_id']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            font_style = xlwt.XFStyle()
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)
            wb.save(response)
            return response
    except Exception as e:
        return HttpResponse("someting went wrong</br>", e)


@login_required
def exportRefundExcel(request, id):
    try:
        if(ReFund.objects.filter(ReFund_For=id).count() < 1):
            return HttpResponse('No ReFund enterys for this tour yet!')
        else:
            rows = ReFund.objects.filter(ReFund_For=id).values_list(
                'Name', 'gender', 'Phone_no1', 'email', 'cancelation_date', 'refund_Amount', 'cancelation_Reason', 'address', 'TripId', 'razorpay_payment_id', 'Payment_Status', 'razorpay_order_id', 'Refund_Status', 'charge_Day', 'charge_percenrate')
            tourIs = Updates.objects.filter(id=id).first()
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition '] = f'attachment;filename={tourIs.Heading}|ReFunds|DowloadedOn__' +\
                str(datetime.datetime.now())+".xls"
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('BookedSlots')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['Name', 'gender', 'Phone_no1', 'email', 'cancelation_date', 'refund_Amount', 'cancelation_Reason', 'address', 'TripId',
                       'razorpay_payment_id', 'Payment_Status', 'razorpay_order_id', 'Refund_Status', 'charge_Day', 'charge_percenrate']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            font_style = xlwt.XFStyle()
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)
            wb.save(response)
            return response
    except Exception as ex:
        return HttpResponse(ex)


def NewsLetter(request):
    if(request.method == 'POST'):
        mailID = request.POST['EmailID']
        NewsLetter_Subscribe = NewsLetter_Subscriber()
        if NewsLetter_Subscriber.objects.filter(Email_Id=mailID).exists():
            return HttpResponse("You already have subscribed to our NewsLetter")
        else:
            NewsLetter_Subscribe.Email_Id = mailID
            NewsLetter_Subscribe.save()
            return HttpResponse("Congrats ,You Have Been Subscribed To Our NewsLetter")


@login_required
def SendNewsletter(request):
    if(request.method == 'POST'):
        file = request.FILES['file']
        filename = file.name
        filename = str(datetime.date.today().strftime("%d-%b-%Y"))+filename
        file_instance = FileSystemStorage(f'{BASE_DIR}/templates/newsletter')
        if FileSystemStorage(f'{BASE_DIR}/templates/newsletter').exists(filename):
            return HttpResponse('file name allready exists please rename your file')
        else:
            domain = request.get_host()
            unsub = f"""
                <div style="text-align: center;background-color: #498553;padding:4px 0;">
                <a href="http://{domain}/Unsubscribe" style="font-size: small; color: #498553;background-color: wheat; padding: 2px 5px;">Unsubscribe</a>
                </div>
                </body>
                </html>
            """
            file_instance.save(filename, file)
            file_edit = open(
                f"{BASE_DIR}/templates/newsletter/{FileSystemStorage().get_valid_name(filename)}", "r+")
            for line in file_edit:
                try:
                    if line.find("</body>") == -1:
                        pass
                    else:
                        file_edit.write('')

                    if line.find("</html>") == -1:
                        pass
                    else:
                        file_edit.write('')
                        file_edit.writelines(unsub)
                except:
                    pass
            file_edit.close()
            return HttpResponse('file uploaded refresh the page to see changes!')
    fs = FileSystemStorage(
        location=f'{BASE_DIR}/templates').listdir('newsletter')
    templates = list()
    for i in fs:
        for j in i:
            try:
                templates.append(f"{FileSystemStorage().get_valid_name(j)}")
            except:
                pass
    mailto = NewsLetter_Subscriber.objects.all().count()

    return render(request, 'newsletter-app-webTemplates/send_newsletter.html', {"templates": templates, 'mailto': mailto})


@login_required
def NewsLatter_sendMails(request):
    if(request.method == 'POST'):
        try:
            template = request.POST['template_selected']
            subject = request.POST['subject']
            mailto = NewsLetter_Subscriber.objects.all()
            data_frame = read_frame(mailto, fieldnames=['Email_Id'])
            mail_list = data_frame['Email_Id'].values.tolist()

            html_message = render_to_string(
                f'newsletter/{FileSystemStorage().get_valid_name(template)}', {})
            plain_message = strip_tags(html_message)
            Mail_From = settings.EMAIL_HOST_USER
            for mail_to in mail_list:
                send_mail(subject, plain_message, Mail_From, [mail_to],
                          html_message=html_message, fail_silently=True)
            return HttpResponse("Mail Sent to NewsLetter Subscribers")
        except Exception as e:
            return HttpResponse(f"""Something went wrong please contact devloper , issue is {e}""")


def Unsubscribe(request):
    if (request.method == "POST"):
        mailId = request.POST['email']
        if NewsLetter_Subscriber.objects.filter(Email_Id=mailId).exists():
            NewsLetter_Subscriber_instance = get_object_or_404(
                NewsLetter_Subscriber, Email_Id=mailId)
            NewsLetter_Subscriber.delete(NewsLetter_Subscriber_instance)
            return HttpResponse("You have now Unsubscribed newsletter now, we will miss you")
        else:
            return HttpResponse("""You are not subscriber.<br><a href='newsletter' class="text-decoration-underline">subscribe Now</a>""")

    return render(request, 'newsletter-app-webTemplates/unsubscribe.html')


def newsletter(request):
    return render(request, "newsletter-app-webTemplates/newsletter_page.html")


@login_required
def Mark_Refunded(request):
    id = request.GET.get('id')
    instance = get_object_or_404(ReFund, id=id)
    if(instance.Refund_Status):
        return HttpResponse(f"ReFunded on {instance.Refund_On}")
    else:
        instance.Refund_Status = True
        instance.Refund_On = datetime.date.today()
        instance.save()

        return HttpResponse(f"ReFunded")


@login_required
def contacted_data(request):
    if request.method == 'GET':
        if 'date' in request.GET:
            date = request.GET['date']
            contacted_data = Contact.objects.filter(
                Contact_on=date).order_by("-Contact_on")
            return render(request, 'admin/table.html', {'data': contacted_data, 'filter': f'contacts of {date}'})
        if 'month' in request.GET:
            month = request.GET['month']
            seprated_data = month.split('-')
            month = seprated_data[1]
            year = seprated_data[0]
            contacted_data = Contact.objects.filter(
                Contact_on__year=year, Contact_on__month=month).order_by("-Contact_on")

            return render(request, 'admin/table.html', {'data': contacted_data, 'filter': f'contacts of month {month},{year}'})

        else:
            pass
    contacted = Contact.objects.order_by('-Contact_on').all()
    return render(request, 'admin/contacted_data.html', {'data': contacted})
