import datetime

from rest_framework import serializers


class DateGreaterEqualToday:
    def __init__(self):
        pass

    def __call__(self, value):
        if value.date() < datetime.date.today():
            raise serializers.ValidationError('Date must be greater or equal to today')
