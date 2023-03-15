from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from twineapi.models import ProjectTeam, Project
from django.contrib.auth.models import User
from datetime import datetime

class TeamView(ViewSet):
    """Twine API team view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single project-team entry

        Returns:
            Response -- JSON serialized employee
        """

        team = ProjectTeam.objects.get(pk=pk)
        serializer = ProjectTeamEntrySerializer(team)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all projects

        Returns:
            Response -- JSON serialized list of projects
        """

        if"project_id" in request.query_params:
            teams = ProjectTeam.objects.filter(project = request.query_params['project_id'])
            serialized = ProjectTeamEntrySerializer(teams, many=True)
        elif"employee_id" in request.query_params:
            teams = ProjectTeam.objects.filter(employee = request.query_params['employee_id'])
            serialized = ProjectTeamSerializer(teams, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)

class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for project leads"""

    class Meta:
        model = User
        fields = ('id', 'employee_account')
        depth = 2

class ProjectTeamEntrySerializer(serializers.ModelSerializer):
    """JSON serializer for project-team entries"""
    employee = EmployeeSerializer(many=False)

    class Meta:
        model = ProjectTeam
        fields = ('id', 'employee', 'project_id')
        depth = 1

class ProjectTeamEntrySerializer(serializers.ModelSerializer):
    """JSON serializer for project-team entries"""
    employee = EmployeeSerializer(many=False)

    class Meta:
        model = ProjectTeam
        fields = ('id', 'employee', 'project')
        depth = 1

class ProjectSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""
    lead = EmployeeSerializer(many=False)

    class Meta:
        model = Project
        fields = ('id', 'title', 'deadline', 'lead')

class ProjectTeamSerializer(serializers.ModelSerializer):
    """JSON serializer for project-team entries"""
    project = ProjectSerializer(many=False)

    class Meta:
        model = ProjectTeam
        fields = ('id', 'employee', 'project')
        depth = 1