from django.contrib import admin
from django.urls import path , include
from updates import urls , views 

urlpatterns = [
    path('',views.update, name='updates'),
    path('/bookslot<int:id>',views.bookslot,name='bookslot'),
    path('/getMoreUpdates<int:number>',views.getMoreUpdates,name='getMoreUpdates'),
]