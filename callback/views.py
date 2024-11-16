from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from django.conf import settings

import json, requests
# Create your views here.

@api_view(["GET"])
def linkedin(request):
    print(request.GET)
    if request.GET["state"] != "xcvusadkfjensa":
        return Response({"status": "Failure: Unauthorised access"})
    token = request.GET["code"]
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    body = {
        "grant_type": "authorization_code",
        "code": token,
        "client_id": "77fb6q9ni6aw0v",
        "client_secret": "h9FRJFiT03uYKhXV",
        "redirect_uri": "https://smrge.anujagrawal.co.in/callback/linkedin"
    }
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=body, headers=header)
    access_token = json.loads(response.content)["access_token"]
    url2 = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
    header2 = {
        "Authorization": f"Bearer {access_token}"
    }
    response2 = requests.get(url2, headers=header2)
    email = json.loads(response2.content)["elements"][0]["handle~"]["emailAddress"]
    HttpResponseRedirect.allowed_schemes.append('smrge')
    return HttpResponseRedirect(f"smrge://smrge.anujagrawal.co.in?email={email}")
