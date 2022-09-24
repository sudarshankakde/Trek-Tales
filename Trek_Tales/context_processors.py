from updates.models import SiteData



sitedata = SiteData.objects.first()

def siteData(request):
    return {'sitedata':sitedata}
