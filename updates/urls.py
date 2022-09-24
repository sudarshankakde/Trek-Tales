from django.contrib import admin
from django.urls import path , include
from updates import urls , views 

urlpatterns = [
    path('',views.update, name='updates'),
    
    # slotBooking
    path('bookslot/<str:slug>',views.bookslot,name='bookslot'),

    # payment id genrate
    path('confirm_booking',views.confirm_booking,name='confirm_booking'), 

    # payment success fail handle   
    path('Payment_Completed',views.Payment_Completed,name='Payment_Completed'),    
    path('Payment_Failed',views.Payment_Failed,name='Payment_Failed'),

    # details and more
    path('details/<str:slug>',views.details,name='tourDetails'),

    path('customize_tour',views.customize_tour,name='customize_tour'),
    
]