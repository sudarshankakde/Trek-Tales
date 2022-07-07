from django.contrib import admin

# Register your models here.
from .models import Testimonials,Updates,BookSlot,SiteData,Contact
admin.site.register(Testimonials)
admin.site.register(Updates)
admin.site.register(BookSlot)
admin.site.register(SiteData)
admin.site.register(Contact)
