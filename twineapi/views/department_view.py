from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from twineapi.models import Department
from django.contrib.auth.models import User
from datetime import datetime

class DepartmentView(ViewSet):
    """Twine API department view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single employee

        Returns:
            Response -- JSON serialized employee
        """

        department = Department.objects.get(pk=pk)
        serializer = DeptSerializer(department)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all projects

        Returns:
            Response -- JSON serialized list of projects
        """
        departments = Department.objects.all()

        serialized = DeptSerializer(departments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class DeptSerializer(serializers.ModelSerializer):
    """JSON serializer for project leads"""

    class Meta:
        model = Department
        fields = ('id', 'name')