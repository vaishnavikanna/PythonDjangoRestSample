from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializer import UserSerializer
from keycloak import KeycloakOpenID
import requests
from urllib.parse import urlencode

# sys.path.append('/home/vaish/.local/lib/python3.10/site-packages')
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/",
                                 client_id="smarterweinberg_keycloak",
                                 realm_name="Kiwi_Users",
                                 client_secret_key="WiZzusfE3GIX6xZOdQLwOOUkbk2ZXBAy")

@api_view(['GET'])
def login(request):
    #redirect_uri = "http://localhost:8000/callback/" + "?" + urlencode(request.GET)
    authorization_url = keycloak_openid.auth_url(
        redirect_uri="http://localhost:8000/callback/",
        scope="openid",
    )
    return redirect(authorization_url)

@api_view(['GET'])
def callback(request):
    # get the authorization code from the request params
    #state = request.GET.get('state')
    code = request.GET.get('code')

    # exchange authorization code for access token and refresh token
    tokens = keycloak_openid.token(code=code)

    # setting access and refresh token in user's session
    request.session['access_token'] = tokens.get('access_token')
    request.session['refresh_token'] = tokens.get('refresh_token')
    #redirect_url = "http://localhost:8000/users/" + "?" + request.GET.urlencode()

    #redirects user to get users page
    return redirect("http://localhost:8000/users/")


@api_view(['GET'])
def getUsers(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def logout(request):
    access_token = request.session.get("access_token")
    logout_url = "http://localhost:8080/realms/kiwi_users/protocol/openid-connect/logout"
    if access_token:
        headers = {
            'Authorization': 'Bearer ' + access_token
        }

    #keycloak_openid.logout(access_token)
    #request.session.flush()

    response = requests.post(logout_url, headers=headers)
    request.session.pop('access_token', None)
    request.session.pop('refresh_token', None)
    return redirect("http://localhost:8000/logoutdisplay/")


@api_view(['POST'])
def logout_display():
    return Response("User successfully logged out")


