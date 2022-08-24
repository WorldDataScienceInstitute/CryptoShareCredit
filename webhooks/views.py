from django.conf import settings as django_settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.core import serializers

from businesses.models import Business
from atm_functions.models import Notification

import json

# Create your views here.


@login_required()
def test(request):
    businesses = Business.objects.all()

    context = {
            'businesses': businesses
            }
            
    return render(request, 'businesses/businesses.html', context)

@login_required()
def get_notifications(request):
    user = request.user

    notifications_queryset = Notification.objects.filter(
        user = user
    ).order_by("-creation_datetime")


    test = {
        "data": json.loads(serializers.serialize('json', notifications_queryset))
    }
    
    return HttpResponse(json.dumps(test), content_type="application/json")