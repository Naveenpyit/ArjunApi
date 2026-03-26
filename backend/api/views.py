from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .authentication import CookieAuthentication
from . import models
from . import serializers
from django.utils import timezone

class UserViews(APIView):

    def get(self,request,pk=None):
        try:
            if pk is None:
                data = models.User.objects.all().order_by('-id')
                serial_data = serializers.UserSerializer(data,many = True).data
            else:
                data = models.User.objects.filter(pk = pk).first()
                serial_data = serializers.UserSerializer(data).data
            return Response({'status':1,'message':'success','data':serial_data})
        except Exception as e:
            return Response({'status':0,'message':str(e)})
        
    def post(self,request):
        try:
            payload = request.data
            serial = serializers.UserSerializer(data = payload)
            if serial.is_valid():
                saved_data = serial.save()
                serial_data = serializers.UserSerializer(saved_data).data
                return Response({'status':1,'message':'User Created Successfully!','data':serial_data})
            return Response({'status':0,'message':'User Created failed!','error':serial.errors})
        except Exception as e:
            return Response({'status':0,'message':str(e)})

COOKIE = { 'httponly': True, 'samesite': 'Lax', 'secure': False, 'path': '/' }
class LoginView(APIView):
    authentication_classes=[]
    def post(self,request):
        try:
            payload = request.data
            user = authenticate(request,email = payload['email'],password = payload['password'])
            if not user:
                return Response({'status':0,'message':'User not found! or Invalid Credentails'})
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            refresh = RefreshToken.for_user(user)
            response = Response({'status':1,'message':'Login Successfully!','data':serializers.UserSerializer(user).data})
            response.set_cookie('access_token',str(refresh.access_token),**COOKIE)
            response.set_cookie('refresh_token',str(refresh),**COOKIE)
            return response
        except Exception as e:
            return Response({'status':0,'message':str(e)})

class CurrentUser(APIView):
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            user = request.user
            return Response({'status':1,'message':'success','data':serializers.UserSerializer(user).data})
        except Exception as e:
            return Response({'status':0,'message':str(e)})

class RefreshTokenView(APIView):
    authentication_classes = []

    def post(self,request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({'status':0,'message':'Token missing or Token Expired'})
            refresh = RefreshToken(refresh_token)
            response = Response({'status':1,'message':'Token Refreshed Successfully!'})
            response.set_cookie('refresh_token',str(refresh_token),**COOKIE)
            response.set_cookie('access_token',str(refresh.access_token),**COOKIE)
            return response
        except Exception as e:
            return Response({'status':0,'message':str(e)})

class LogoutView(APIView):
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({'status': 0, 'message': 'Token not exist'}, status=400)
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response({'status':1,'message':'Logout Successfully!'})
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        except Exception as e:
            return Response({'status':0,'message':str(e)})