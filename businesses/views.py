from django.conf import settings as django_settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import Http404
# Create your views here.


def test(request):
    raise Http404()