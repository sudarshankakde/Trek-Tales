from updates.models import SiteData
from Trek_Tales import settings


sitedata = SiteData.objects.first()

def siteData(request):
    return {'sitedata': sitedata, 'devloper': settings.Devloper}
