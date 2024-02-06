import os
import time

import pandas as pd
from rest_framework import serializers

from .models import TocsCSVRow, TocsEvent


class TocsEventSerialiser(serializers.ModelSerializer):
    class Meta:
        model=TocsEvent 
        fields='__all__'
class TocsCSVRowSerialiser(serializers.ModelSerializer):
    class Meta:
        model=TocsCSVRow 
        fields='__all__'





