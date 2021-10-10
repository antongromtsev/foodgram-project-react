from django.contrib.auth import get_user_model 
from rest_framework import serializers 

User = get_user_model() 


def is_time_int(value): 
    if User.objects.filter(email=value).exists(): 
        raise serializers.ValidationError( 
            'A user with that email already exists.' 
        ) 
