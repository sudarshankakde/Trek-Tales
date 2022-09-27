import requests
from updates.models import *


def latest_tour():
    try:
        upcoming_tour = Updates.objects.filter(TourIsNotExpire=True).all()
        print(str(upcoming_tour))
        return True
    except Exception as e:
        print(e)
    return False
