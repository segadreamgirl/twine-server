from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from twineapi.models import Ticket, TicketFlag, Project
from django.contrib.auth.models import User

class TicketView(ViewSet):
    """Twine API employee view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single ticket

        Returns:
            Response -- JSON serialized ticket
        """
        ticket = Ticket.objects.get(pk=pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all tickets

        Returns:
            Response -- JSON serialized list of tickets
        """

        tickets=[]
        
        if "project_id" in request.query_params:
            tickets = Ticket.objects.filter(project = request.query_params['project_id'])
            if "unassigned" in request.query_params:
                tickets = Ticket.objects.filter(project= request.query_params['project_id'], assignee__isnull=True)
            if "assigned" in request.query_params:
                tickets = Ticket.objects.filter(project= request.query_params['project_id'], assignee__isnull=False).exclude(completed = True)
            if "completed" in request.query_params:
                tickets = Ticket.objects.filter(project= request.query_params['project_id'],completed=True)
        else:
            tickets = Ticket.objects.all()

        serialized = TicketSerializer(tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handles POST requests for tickets
        Returns:
            Response: JSON serialized representation of newly created ticket"""

        new_ticket = Ticket()
        new_ticket.title = request.data['title']
        new_ticket.description = request.data['description']
        new_ticket.project= Project.objects.get(pk=request.data['project'])
        new_ticket.completed = request.data['completed']

        new_ticket.save()

        serialized = TicketSerializer(new_ticket, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for tickets

        Returns:
            nothing
        """

        edit_ticket = Ticket.objects.get(pk=pk)
        edit_ticket.title = request.data['title']
        edit_ticket.description = request.data['description']
        edit_ticket.assignee = User.objects.get(pk=request.data['assignee'])
        edit_ticket.completed = request.data['completed']

        edit_ticket.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle PUT requests for service tickets

        Returns:
            Response: None with 204 status code
        """
        delete_ticket = Ticket.objects.get(pk=pk)
        delete_ticket.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class AssigneeUserSerializer(serializers.ModelSerializer):
    """JSON serializer for ticket users"""
    class Meta:
        model = User
        fields = ('id', 'employee_account')
        depth=2

class FlagSerializer(serializers.ModelSerializer):
    """JSON serializer for ticket users"""
    class Meta:
        model = TicketFlag
        fields = ('id', 'flag')
        depth=1

class TicketSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    assignee = AssigneeUserSerializer(many=False)
    ticket_flags = FlagSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'description', 'project', 'assignee', 'completed', 'ticket_flags' )