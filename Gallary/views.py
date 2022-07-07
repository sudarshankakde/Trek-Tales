from django.shortcuts import render
from Gallary.models import Memories
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse




# Create your views here.
def gallary(request):
    memories = Memories.objects.order_by("-photo_taken_on_date")[0:6]
    return render(request, 'gallary.html',{'Memories':memories})


def likeMemory(request,id):
    Memorie = get_object_or_404(Memories,id=id)
    Memorie.likes = Memorie.likes + 1
    Memorie.save()
    return redirect('gallary')

def loadMore(request,number):
    toSend = number+6
    CurrentPost = number
    photos = Memories.objects.order_by("-photo_taken_on_date")[CurrentPost:toSend]
    return JsonResponse({"Images":list(photos.values())})
    