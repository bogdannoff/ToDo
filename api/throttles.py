from rest_framework import throttling


class CustomUserRateThrottle(throttling.UserRateThrottle):
    rate = '3/min'