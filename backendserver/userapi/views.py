from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import data
from . serializers import dataSerializer

class dataList(APIView):
    def get(self, request, user_id = None):
        if user_id is None:
            getquery = data.objects.all()
        else:
            getquery = data.objects.filter(user_id=user_id)
        serializer = dataSerializer(getquery, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = dataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        # Get the data object based on the user_id
        data_object = get_object_or_404(data, user_id=user_id)

        # Update the data object with the new data from the request
        serializer = dataSerializer(data_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        # Get the data object based on the user_id
        # data_object = get_object_or_404(data, user_id=user_id)

        # # Delete the data object
        # data_object.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

        #----------------------shortcut------------------------#

        # Retrieve all user objects from the database
        users = data.objects.all()

        # Loop through each user and update the attribute_to_update field
        for user in users:
            user.dailyT1 = "wonka"
            user.dailyT2 = "wonka"
            user.dailyT3 = "wonka"
            user.dailyT4 = "wonka"
            user.weekT1 = "willi"
            user.weekT2 = "willi"
            user.weekT3 = "willi"
            user.weekT4 = "willi"
            user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)