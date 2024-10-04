from django.shortcuts import render
from django.http import HttpResponse
from .models import Magaza


async def test_view(request):
    data = await Magaza.objects.filter(ad="test").afirst()
    print(data)
    return HttpResponse("Hello, World!")