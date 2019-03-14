from django.shortcuts import render
from api.serializers import (
    GrillImageSerializer,
    GrillSerializer,
    BookingSerializer,
    UserCreateSerializer
)
from rest_framework import generics
from api.models import *

from rest_framework.generics import (
    ListCreateAPIView,CreateAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
) 


# Create your views here.

'''
Views of Rest framework
'''
class UserCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

class GrillListCreate(generics.ListCreateAPIView):
    queryset = Grill.objects.all()
    serializer_class = GrillSerializer
    
    def perform_create(self,serializer): 
        serializer.save(owner=self.request.user)

class GrillRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
	queryset = Grill.objects.all()
	serializer_class = GrillSerializer

class GrillImageListCreate(generics.ListCreateAPIView):
	queryset = Grill.objects.all()
	serializer_class = GrillSerializer
	

class GrillImageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
	queryset = GrillImage.objects.all()
	serializer_class = GrillImageSerializer

class BookingListCreate(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
	

class BookingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer