from django.shortcuts import render
from django.http import HttpResponse
from .models import Tips

# Create your views here.
def index(request):
    # return HttpResponse('Hello from tips')

    tips = Tips.objects.all()[:10]

    context = {
        'title': 'Latest Tips',
        'tips': tips
    }
    return render(request, 'tips/index.html', context)

def details(request, id):
    tip = Tips.objects.get(id=id)

    context = {
        'tip': tip
    }
    return render(request, 'tips/details.html', context)