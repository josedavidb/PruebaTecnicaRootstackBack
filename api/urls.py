from django.urls import path, re_path, include
from django.conf.urls import url
from rest_framework import routers

from . import views
from .views import UserCreateAPIView

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    url(r'^grill/$',views.GrillListCreate.as_view()),
    url(r'^grill/(?P<pk>\d+)/$',views.GrillRetrieveUpdateDestroy.as_view()),
    url(r'^grillimage/$',views.GrillImageListCreate.as_view()),
    url(r'^grillimage/(?P<pk>\d+)/$',views.GrillImageRetrieveUpdateDestroy.as_view()),
    url(r'^booking/$',views.BookingListCreate.as_view()),
    url(r'^booking/(?P<pk>\d+)/$',views.BookingRetrieveUpdateDestroy.as_view()),
]