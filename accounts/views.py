from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny

from accounts.serializers import SignInSerializer,SignUpSerializer,UserSerializer
# Create your views here.
class SigninView(APIView):
    permission_classes=[AllowAny]
    def post(self,*args,**kwargs):
        serializer=SignInSerializer(data=self.request.data)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SignupView(APIView):
    authentication_classes=[]
    permission_classes=[AllowAny]
    def post(self,*args,**kwargs):
        serializer=SignUpSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=UserSerializer
    queryset=User.objects.all()
    def get_queryset(self):
        return User.objects.filter(is_superuser=False)