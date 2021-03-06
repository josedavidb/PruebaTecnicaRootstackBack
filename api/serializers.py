from rest_framework import serializers,exceptions
from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    IntegerField,
    StringRelatedField,
)
from rest_framework.exceptions import ValidationError

from django.db.models import Q
from api.models import *

User = get_user_model()


#Serializer for user registration

class UsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'pk'
        ]
        
class UserCreateSerializer(ModelSerializer):

    '''
    #Serializer for user registration
    '''
    birthdate = serializers.DateField()
    gender = serializers.CharField()
    confirm_email = serializers.CharField()
    confirm_password = serializers.CharField(write_only=True)
    zip_code = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'confirm_email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'birthdate',
            'gender',
            'zip_code'
        ]

        #Variable to don't allow read password, write only
        extra_kwargs = {'password': {
                        'write_only': True
        }, 'confirm_password': {
            'write_only' : True
        }}

    def validate_password(self,value):
        data = self.get_initial()
        pass2 = data.get('confirm_password')
        pass1 = value
        if pass1 != pass2:
            raise ValidationError('Password doesnt match with confirmation' )
        return value

    def validate_gender(self,value):
        if (value != 'M' and value!= 'F' and value != 'O'):
            raise ValidationError('The gender is incorrect')
        return value

    def validate_email(self,value):
        data = self.get_initial()
        email2 = data.get('confirm_email')
        email1 = value
        if email1 != email2:
            raise ValidationError('Email doesnt match with confirmation')
        return value

    #Function to validate that user doesnt already exist
    def validate(self,data):
        email = data['email']
        username = data['username']
        if '@' in username:
            raise ValidationError('This user is invalid') 
        user_qs_email= User.objects.filter(email=email)
        user_qs_username = User.objects.filter(username=username)
        if user_qs_email.exists():
            raise ValidationError('This email already exists')
        if user_qs_username.exists():
            raise ValidationError('This user already exists')
        return data

    #Override function create to save user correctly

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        user_obj = User(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
        )
        user_obj.set_password(password)
        user_obj.save()
        print('Aja acabo de guardar el usuario')
        user_obj.profile.birthdate = validated_data['birthdate']
        print('Aja acabo de guardar el birthdate')
        user_obj.profile.gender = validated_data['gender']
        print('Aja acabo de guardar el genero')
        user_obj.profile.zip_code = validated_data['zip_code']
        print('Aja acabo de guardar el zip code')
        user_obj.save()
        return validated_data

class GrillSerializer(serializers.ModelSerializer):
    """
    Consist in the serializer of model Grill.
    Fields that are going to pass: model, description, zip code, width, height, weight, color, owner
    """
    owner = UsernameSerializer(required=False)

    class Meta:
        model = Grill
        fields = ('pk','model','description','zip_code','width','height','weight','color','owner')
        read_only_fields = ('owner',)

class GrillImageSerializer(serializers.ModelSerializer):
	"""
	Consist in the serializer of model GrillImage.
	Fields that are going to pass: grill, image
	"""
	class Meta:
		model = GrillImage
		fields = ('grill','image')

class BookingSerializer(serializers.ModelSerializer):
    """
    Consist in the serializer of model Booking.
    Fields that are going to pass: grill, user, date, hour_start, hour_end
	"""

    class Meta:
        model = Booking
        fields = ('pk','grill','user','date','hour_start','hour_end')
        read_only_fields = ('user',)
    
    def validate(self,data):
        hour_start = data['hour_start']
        hour_end = data['hour_end']
        date = data['date']
        grill = data['grill']
        if hour_start > hour_end:
            raise ValidationError('The hour start cant be higher than hour end') 
        booking_qs1 = Booking.objects.filter(grill=grill,date=date, hour_start__lte = hour_end, hour_end__gte = hour_end)
        booking_qs2 = Booking.objects.filter(grill=grill,date=date, hour_start__lte = hour_start, hour_end__gte = hour_start)
        booking_qs3 = Booking.objects.filter(grill=grill,date=date, hour_start__gte = hour_start, hour_end__lte = hour_end)


        booking_qs = booking_qs1 | booking_qs2 | booking_qs3
        if booking_qs.exists():
            raise ValidationError('The grill already reservated for that date and that specific hour')
        return data
    


    