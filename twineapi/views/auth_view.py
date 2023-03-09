from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a player

    Method arguments:
        request -- The full HTTP request object
    '''
    email = request.data['email']
    password = request.data['password']
    authenticated_user = authenticate(username=email, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        # this is where we update what gets sent back to the client for localStorage.
        # also at the bottom of this module for during a user registration

        data = {
            'valid': True,
            'id': authenticated_user.id,
            'first_name': authenticated_user.first_name,
            'last_name': authenticated_user.last_name,
            'token': token.key
            }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new player for authentication

    Method arguments:
        request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    try:
        User.objects.get(email=request.data['email'])
        data = {'message': 'This email is already in use'}
    except User.DoesNotExist:

        new_user = User.objects.create_user(
            username=request.data['email'],
            password=make_password(request.data['password']),
            email=request.data['email'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
        )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)
        # Return the token to the client
        # this is where we update what gets sent back to the client for localStorage
        data = {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'token': token.key
            }
    return Response(data)


class EmployeeAccountSerializer(serializers.ModelSerializer):
    """JSON serializer for project leads"""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'employee_account')
        depth = 1