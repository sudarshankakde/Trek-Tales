from django.contrib import admin

# Register your models here.
from .models import Testimonials,Updates,BookSlot,SiteData,Contact,Organizer,Tags,NewsLetter_Subscriber,ReFund,customized_tour

class UpdatesAdmin(admin.ModelAdmin):
    list_display = ['id','Organizer','price','location','tour_on_date']
admin.site.register(Updates,UpdatesAdmin)


class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ['id','ReviewBy','profession','date_added']
admin.site.register(Testimonials,TestimonialsAdmin)

class BookSlotAdmin(admin.ModelAdmin):
    list_display = ['Name','slotFor','TripId','razorpay_payment_id']
admin.site.register(BookSlot,BookSlotAdmin)


admin.site.register(SiteData)
admin.site.register(Contact)




class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['Name','telephone','mail']
admin.site.register(Organizer,OrganizerAdmin)

class TagsAdmin(admin.ModelAdmin):
    list_display = ['id','Tag']
admin.site.register(Tags,TagsAdmin)

admin.site.register(NewsLetter_Subscriber)
admin.site.register(ReFund)


class customized_tourAdmin(admin.ModelAdmin):
    list_display = ['name','trek_name','group_size','no_of_day','phone']
admin.site.register(customized_tour,customized_tourAdmin)


