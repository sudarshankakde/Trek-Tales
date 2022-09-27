import django
import os
import requests
import pandas
import telegram
os.environ['DJANGO_SETTINGS_MODULE'] = 'Trek_Tales.settings'
django.setup()

from django.contrib.sites.shortcuts import get_current_site
from telegram.ext import *
from updates.models import *
from Trek_Tales.settings import *

API_KEY = "5602490202:AAGIzZkE2f1B3E0FvvhSxkgvOhMRiPFhiDw"


def handle_message(update, context):
    message = str(update.message.text).lower()
    username = update['message']['chat']['first_name']
    chat_id = update['message']['chat']['id']
    sitedata =  SiteData.objects.order_by('-id').first()
    print(message)

    if message in ('hii', 'hi','hello', 'namste', 'hey', 'hey!', 'hello!'):
        update.message.reply_text(f"Hi , {username}")

    if message in ('latest tour', 'upcoming event', 'tour', 'tours'):
        upcoming_tour = Updates.objects.filter(TourIsNotExpire=True).all()
        if upcoming_tour.count() == 0:
            update.message.reply_text('currently there are no upcoming tour!')
        else:
            update.message.reply_text(
                f'there are {upcoming_tour.count()} upcoming tours.')
            for tour in upcoming_tour.iterator():
                sr = pandas.Series([tour.price, str(tour.tour_on_date), tour.location, tour.slorts])
                idx = ['Price 💳', 'tour on 📆', 'venus 🌄', 'slorts remaing 👱‍♂️']
                sr.index = idx
                message = f"""<b>{tour.Heading}</b>

Price : <u>{tour.price}</u>
Tour on : <u>{tour.tour_on_date}</u>
venus : <u>{tour.location}</u>
slorts remaing : <u>{tour.slorts}</u>

<a href="{domain}/tours/details/{tour.slug}">More Details</a>
<a href="{domain}/tours/bookslot/{tour.slug}">Book Now</a>"""
                print(f"{domain}{tour.Tumbnail.url}")
                # update.message.reply_photo(f"{domain}{tour.Tumbnail.url}")
                update.message.reply_text(message,parse_mode=telegram.ParseMode.HTML)

    if message in ('what can you do?', 'what can you do', 'what you do?', 'what you do'):
        update.message.reply_text(
            'I can tell you our upcoming tour,about our company and details about your booking!')

    if message in ("my booking", "booking detail", "payment Details"):
        update.message.reply_text('send your trip Id or your payment Id')
    
    if message in ('contact'):
        update.message.reply_contact(f"+91{sitedata.SecondNumber}", "Kiran Jadhav")


  


if __name__ == '__main__':
    print("bot started")
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling(1.0)
    updater.idle()
