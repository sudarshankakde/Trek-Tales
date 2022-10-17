from django.shortcuts import render
from Gallary.models import Memories
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from updates.models import Updates
from django.contrib.auth.decorators import login_required
import os

# Create your views here.


def gallary(request):
    reponse_data = Memories.objects.order_by('-uploaded_on').all()
    tours = Updates.objects.order_by('-tour_on_date').all()
    peginator = Paginator(reponse_data, 15)
    page_number = request.GET.get('page', 1)
    memories = peginator.get_page(page_number)
    if(request.htmx):
        if 'selected_tour' in request.GET:
            selected_tour = request.GET['selected_tour']
            if selected_tour == 'all_tour':
                return render(request, 'gallary/imageCard.html', {'memories': memories, 'tours': tours})
            else:
                memories = Memories.objects.filter(
                    photo_taken_on_tour=selected_tour)
                if memories.count() == 0:
                    return HttpResponse(f"""No Memories Of<b class="text-capitalize">{Updates.objects.filter(id=selected_tour).first().Heading}</b>Tour""")
                return render(request, 'gallary/imageCard.html', {'memories': memories})
        else:
            return render(request, 'gallary/imageCard.html', {'memories': memories})
    return render(request, 'gallary.html', {'memories': memories, 'tours': tours})


@login_required
def upload_images(request):
    tours = Updates.objects.all()
    if(request.method == 'POST'):
        Images = request.FILES.getlist("Images")
        photographer = request.POST['photographer']
        TourSelect = request.POST['TourSelect']
        if TourSelect == 'notSeleted':
            for Memorie in Images:
                Memories(author=photographer, photos_taken=Memorie).save()
                print(Memorie)
            return HttpResponse(f"{len(Images)}Memorie(s) uploaded! Without Tour Details")
        else:
            for Memorie in Images:
                os.rename(Memorie, f'{tourName}-{photographer}')
                Memories(author=photographer, photo_taken_on_tour=get_object_or_404(
                    Updates, id=TourSelect), photos_taken=Memorie).save()
                print(Memorie)
            return HttpResponse(f"{len(Images)}Memorie(s) uploaded!")
    return render(request, 'gallary/uploadImages.html', {'tours': tours})
