from django.shortcuts import render
from rest_framework import generics

from .models import *
from .serializer import *


class TocsEventListCreate(generics.ListCreateAPIView):
    queryset=TocsEvent.objects.all().order_by("id")[:10]
    serializer_class =TocsEventSerialiser


class  TocsEventRetrieveUpdateDelete(generics.RetrieveAPIView):
    queryset=TocsEvent.objects.all()
    serializer_class=TocsEventSerialiser
