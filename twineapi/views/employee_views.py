from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from twineapi.models import Employee, Department
from django.contrib.auth.models import User
from datetime import datetime

class EmployeeView(ViewSet):
    """Twine API employee view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single employee

        Returns:
            Response -- JSON serialized employee
        """
        employee = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all employees

        Returns:
            Response -- JSON serialized list of tickets
        """

        employees=[]

        if "department_id" in request.query_params:
            employees = Employee.objects.filter(department = request.query_params['department_id'])
        else:
            employees = Employee.objects.all()

        serialized = EmployeeSerializer(employees, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class EmployeeUserSerializer(serializers.ModelSerializer):
    """JSON serializer for employee users"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

class EmployeeDeptSerializer(serializers.ModelSerializer):
    """JSON serializer for employee parks"""
    class Meta:
        model = Department
        fields = ('id', 'name','color')

class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    user = EmployeeUserSerializer(many=False)
    department = EmployeeDeptSerializer(many=False)

    class Meta:
        model = Employee
        fields = ('id', 'user', 'department', 'profile_pic')
        depth = 1