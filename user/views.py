from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.serializer import InterestSerializer, UserSerializer
from django.utils.crypto import get_random_string
from django.conf import settings

import boto3
import json
import base64
from user.utils import get_coords
from geopy.distance import geodesic
from .models import Interest, UserProfile
from jose import jwt
import requests

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Create your views here.
@api_view(["POST"])
def register_user(request):
    print(request.data)
    user_data = request.data
    # print("User Data", user_data)
    # user_data = json.loads(str(user_data))
    token = get_random_string(length=128)
    # user_data["token"] = token
    print(user_data)
    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        user = serializer.save(token=token)
        for interest in user_data["interests"]:
            if Interest.objects.filter(id=interest["id"]).exists():
                obj = Interest.objects.get(id=interest["id"])
                user.interests.add(obj)
        user.save()
        print("Success")
        return Response({'status': 'Success', 'data': token})
    else:
        print("Failure", serializer.errors)
        return Response({'status': "Failure", 'data': str(serializer.errors)})

@api_view(["GET"])
def generate_otp(request):
    print(request.GET)
    mobile = request.GET["mobile"]
    client = boto3.client('pinpoint', region_name="ap-south-1")
    ref_id = get_random_string(10)
    with open('aws_application', 'r') as f:
        l = f.readlines()
        applicationID = l[0].split('=')[-1].strip()
    client.send_otp_message(
        ApplicationId=applicationID,
        SendOTPMessageRequestParameters= {
            'AllowedAttempts': 1,
            'BrandName': 'SMRGE',
            'Channel': 'SMS',
            'DestinationIdentity': f'+91{mobile}',
            'OriginationIdentity': 'SMRGE-ID',
            'ReferenceId': ref_id
        }
    )
    return Response({'status': "Success", 'data': ref_id})

@api_view(["GET"])
def generate_otp_extra(request):
    print(request.GET)
    mobile = request.GET["mobile"]
    client = boto3.client('pinpoint', region_name="ap-south-1")
    ref_id = get_random_string(10)
    # with open('aws_application', 'r') as f:
      #  l = f.readlines()
       # applicationID = l[0].split('=')[-1].strip()
    applicationID = '123'
    client.send_otp_message(
        ApplicationId=applicationID,
        SendOTPMessageRequestParameters= {
            'AllowedAttempts': 1,
            'BrandName': 'SMRGE',
            'Channel': 'SMS',
            'DestinationIdentity': f'{mobile}',
            'OriginationIdentity': 'SMRGE-ID',
            'ReferenceId': ref_id
        }
    )
    return Response({'status': "Success", 'data': ref_id})

@api_view(["GET"])
def verify_otp(request):
    mobile = request.GET["mobile"]
    ref_id = request.GET["ref_id"]
    otp = request.GET["otp"]
    with open('aws_application', 'r') as f:
        l = f.readlines()
        applicationID = l[0].split('=')[-1].strip()
    client = boto3.client('pinpoint', region_name="ap-south-1")
    response = client.verify_otp_message(
        ApplicationId=applicationID,
        VerifyOTPMessageRequestParameters={
            'DestinationIdentity': f'+91{mobile}',
            'Otp': otp,
            'ReferenceId': ref_id
        }
    )
    if response["VerificationResponse"]["Valid"] == True:
        return Response({"status": "Success", "data": "OTP Valid"})
    return Response({'status': 'Failure', 'data': "OTP Invalid"})

@api_view(["GET"])
def verify_otp_extra(request):
    mobile = request.GET["mobile"]
    ref_id = request.GET["ref_id"]
    otp = request.GET["otp"]
    with open('aws_application', 'r') as f:
        l = f.readlines()
        applicationID = l[0].split('=')[-1].strip()
    client = boto3.client('pinpoint', region_name="ap-south-1")
    response = client.verify_otp_message(
        ApplicationId=applicationID,
        VerifyOTPMessageRequestParameters={
            'DestinationIdentity': f'{mobile}',
            'Otp': otp,
            'ReferenceId': ref_id
        }
    )
    if response["VerificationResponse"]["Valid"] == True:
        return Response({"status": "Success", "data": "OTP Valid"})
    return Response({'status': 'Failure', 'data': "OTP Invalid"})

@api_view(["POST"])
def update_profile(request):
    print("start", request.data, type(request.data))
    if type(request.data) == str:
        data = json.loads(json.loads(request.data))
        print(type(data))
    else:
        data = request.data
        # print(type(data), "In else")
    # print(data.keys)
    user = UserProfile.objects.get(token=data["token"])
    # print(data)
    serializer = UserSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        user = serializer.save()
        # print(user.__dict__)
        return Response({'status': 'Success', 'data': "User updated Successfully"})
    else:
        print(serializer.errors)
        return Response({'status': "Failure", 'errros': serializer.error_messages})

@api_view(["GET"])
def get_profiles(request):
    print(request.GET)
    lat = float(request.GET["lat"])
    lon = float(request.GET["lon"])
    min_age = int(request.GET["min_age"])
    max_age = int(request.GET["max_age"])
    distance = float(request.GET['distance'])
    token = request.GET["token"]
    user = UserProfile.objects.get(token=token)
    min_lat, max_lat, min_lon, max_lon = get_coords(lat, lon, distance/1000)
    queryset = UserProfile.objects.exclude(token=token)
    queryset = queryset.exclude(id__in=user.saved_profiles.all())
    queryset = queryset.filter(last_lat__gte=min_lat, last_lat__lte=max_lat, last_lon__gte=min_lon, last_lon__lte=max_lon)
    users = queryset.all()

    print("=============================")
    print(min_lat, max_lat, min_lon, max_lon)
    print("=============================")

    # for i in range(len(users)):
    #     if (users[i].age < min_age) or (users[i].age > max_age):
    #         users.exclude(token=users[i].token)
    data = UserSerializer(users, many=True)
    for user in data.data:
        user["distance"] = geodesic((lat, lon), (user["last_lat"], user["last_lon"])).km * 1000
    return JsonResponse({'status': 'Success', 'data': data.data}, safe=False)

@api_view(["GET"])
def get_user_profile(request):
    # print(request.GET)
    user = UserProfile.objects.get(token=request.GET["token"])
    data = UserSerializer(user)
    return JsonResponse({'status': 'Success', 'data': data.data}, safe=False)

@api_view(["GET"])
def get_token(request):
    # print(request.GET)
    key = settings.APP_SECRET
    private_key = serialization.load_pem_private_key(
         key.encode('UTF-8'),
         password=None)
    id = private_key.decrypt(
            base64.b64decode(request.GET["data"]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    id = str(id, "utf-8")
    if request.GET["medium"] == "email":
        print("Email Verification", id)
        if UserProfile.objects.filter(email=id).exists():
            user = UserProfile.objects.filter(email=id).first()
            return JsonResponse({'status': 'Success', 'data': user.token}, safe=False)
        else:
            return JsonResponse({'status': 'Failure', 'data': "New user"}, safe=False)
    elif request.GET["medium"] == "mobile":
        print("Mobile Verification")
        if UserProfile.objects.filter(mobile=id).exists():
            user = UserProfile.objects.filter(mobile=id).first()
            return JsonResponse({'status': 'Success', 'data': user.token}, safe=False)
        else:
            return JsonResponse({'status': 'Failure', 'data': "New user"}, safe=False)
    else:
        return JsonResponse({'status': 'Failure', 'data': "Invalid medium"}, safe=False)

@api_view(["GET"])
def save_profile(request):
    print(request.GET)
    saved_user = UserProfile.objects.get(pk=request.GET['id'])
    user = UserProfile.objects.get(token=request.GET['token'])
    if user.saved_profiles.count() == 20:
        return Response({'status': 'Failure', 'data': 'Too many saved profiles'})
    user.saved_profiles.add(saved_user)
    return Response({'status': 'Success', 'data': 'Profile added successfully'})

@api_view(["GET"])
def remove_profile(request):
    print(request.GET)
    saved_user = UserProfile.objects.get(pk=request.GET['id'])
    user = UserProfile.objects.get(token=request.GET['token'])
    if saved_user in user.saved_profiles:
        user.saved_profiles.remove(saved_user)
    return Response({'status': 'Success', 'data': 'User removed successfully'})

@api_view(["GET"])
def get_all_interests(request):
    data = InterestSerializer(Interest.objects.all(), many=True)
    print(data)
    return JsonResponse({'status': 'Success', 'data': data.data}, safe=False)

@api_view(["GET"])
def get_saved_profiles(request):
    print(request.GET)
    users = UserProfile.objects.get(token=request.GET["token"]).saved_profiles.all()
    data = UserSerializer(users, many=True)
    return JsonResponse({'status': 'Success', 'data': data.data}, safe=False)

@api_view(["GET"])
def google_verification(request):
    # print(request.GET)
    token = request.GET["token"]
    jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
    jwks = requests.get(jwks_url).json()

    # Get the key that was used to sign the JWT
    kid = jwt.get_unverified_header(token).get("kid")
    key = next(k for k in jwks["keys"] if k["kid"] == kid)

    # Verify the signature of the JWT using the key
    try:
        decoded_token = jwt.decode(token, key, algorithms=["RS256"], audience='801489613991-qf7et6q1207snfeq9ot6fgs68la2gupb.apps.googleusercontent.com')
        print(decoded_token)
        return JsonResponse({'status': 'Success', 'data': decoded_token}, safe=False)
    except jwt.exceptions.DecodeError as e:
        print(f"Error decoding JWT: {e}")
        return JsonResponse({'status': 'Failure', 'data': e}, safe=False)
