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
from django.urls import path , include
from updates import urls , views 
from Trek_Tales import views
from django.conf import settings
from django.conf.urls.static import static
from Gallary import views as gallaryViews

urlpatterns = [
    path('admin/', admin.site.urls),
    # home
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    #contact
    path('contact',views.contact,name='contact'),
    #Cancelation
    path('cancelation',views.cancelation,name='cancelation'),
    # gallary
    path('gallary',gallaryViews.gallary,name='gallary'),
    path('gallary/like/<int:id>',gallaryViews.likeMemory,name='likeMemory'),
    path('gallary/getImages<int:number>',gallaryViews.loadMore,name="loadMore"),
    # updates
    path('updates',include('updates.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

