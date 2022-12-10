from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import SignInSerializer,SignUpSerializer
# Create your views here.
class SigninView(APIView):
    def post(self,*args,**kwargs):
        serializer=SignInSerializer(data=self.request.data)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SignupView(APIView):
    def post(self,*args,**kwargs):
        serializer=SignUpSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)