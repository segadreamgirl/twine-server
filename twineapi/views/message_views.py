from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from twineapi.models import Employee, Department, Message
from django.contrib.auth.models import User
from datetime import datetime

class MessageView(ViewSet):
    """Twine API message view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single employee

        Returns:
            Response -- JSON serialized employee
        """

        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all messages

        Returns:
            Response -- JSON serialized list of messages
        """
        if "sender_id" in request.query_params:
            messages = Message.objects.filter(sender = request.query_params['sender_id'])
        elif "receiver_id" in request.query_params:
            messages = Message.objects.filter(receiver = request.query_params['receiver_id'])
        else:
            messages = Message.objects.all()

        serialized = MessageSerializer(messages, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users associated with a conversation"""

    class Meta:
        model = User
        fields = ('id', 'employee_account')
        depth = 2

class MessageSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    sender = UserSerializer(many=False)
    receiver = UserSerializer(many=False)

    class Meta:
        model = Message
        fields = ('body','sender','receiver','time_sent')
        depth = 1