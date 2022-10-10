"""Trek_Tales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from updates import urls, views
from Trek_Tales import views
from Trek_Tales import settings
from Gallary import views as gallaryViews
from django.urls import re_path as url
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_links', views.admin_links, name='admin_links'),
    path('contacted_data', views.contacted_data, name='contacted_data'),
    path('ShowBookings/', views.ShowBookings, name='ShowBookings'),
    path('ShowBookings/<int:id>', views.ShowBookingsOfId, name="ShowBookingsOfId"),
    path('exportExcel/<int:id>', views.exportExcel, name='exportExcel'),
    path('exportRefundExcel/<int:id>',
         views.exportRefundExcel, name='exportRefundExcel'),
    path('NewsLetter', views.NewsLetter, name='NewsLetter'),
    path('SendNewsletter', views.SendNewsletter, name='SendNewsletter'),
    path('NewsLatter_sendMails', views.NewsLatter_sendMails,
         name='NewsLatter_sendMails'),
    path('unsubscribe', views.Unsubscribe, name="unsubscribe"),
    path('newsletter', views.newsletter, name="newsletter"),

    # home
    path('', views.home, name='home'),
    path('home', views.home, name='home'),

    # contact
    path('contact', views.contact, name='contact'),
    # Cancelation
    path('cancelation', views.cancelation, name='cancelation'),

    # Refund
    path('Mark_Refunded', views.Mark_Refunded, name='Mark_Refunded'),

    # gallary
    path('gallary', gallaryViews.gallary, name='gallary'),

    # about us
    path('aboutUs', views.aboutUs, name='aboutUs'),


    # updates
    path('tours/', include('updates.urls')),

    # serve
    url(r'^DataBase/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATICFILES_DIRS}),
    # url(r'^static/(?P<path>.*)$', serve,
    #     {'document_root': settings.STATIC_ROOT}),
]

handler404 = 'Trek_Tales.views.error_404_view'
handler500 = 'Trek_Tales.views.error_500_view'
