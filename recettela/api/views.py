from django.contrib.auth.models import User, Group
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, status
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recettela.api.serializers import UserSerializer, GroupSerializer, FoodSerializer
from recettela.models import Food


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@permission_classes([IsAuthenticated])
class ListCreateFoodView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return Food.objects.filter(fridge=self.request.user).order_by('expiration_date')

    def create(self, request, *args,
               **kwargs):  # don't need to `self.request` since `request` is available as a parameter.

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(fridge=request.user)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, food_pk, format=None): #TODO verifier de ne pas supp celui dun autre
        object = self.get_object(food_pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def food_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Food.objects.get(pk=pk)
    except Food.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = FoodSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = FoodSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)