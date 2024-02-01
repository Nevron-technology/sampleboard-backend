from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User, Group

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions, status


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            group = user.groups.first()
            id = user.id 
        except:
            group = None
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'group': str(group),
            'id' : id 
        })