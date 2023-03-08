from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from twineapi.models import Employee, Department, Project
from django.contrib.auth.models import User
from datetime import datetime

class ProjectView(ViewSet):
    """Twine API project view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single employee

        Returns:
            Response -- JSON serialized employee
        """

        project = Project.objects.get(pk=pk)
        serializer = IndividualProjectSerializer(project)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all projects

        Returns:
            Response -- JSON serialized list of projects
        """

        projects = Project.objects.all()

        serialized = ProjectSerializer(projects, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class LeadSerializer(serializers.ModelSerializer):
    """JSON serializer for project leads"""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'employee_account')
        depth = 1

class ProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    lead = LeadSerializer(many=False)

    class Meta:
        model = Project
        fields = ('id', 'title', 'deadline', 'lead')

class IndividualProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    lead = LeadSerializer(many=False)

    class Meta:
        model = Project
        fields = ('id', 'title', 'deadline', 'lead','project_tickets')
        depth = 1