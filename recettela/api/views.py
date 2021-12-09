from django.contrib.auth.models import User, Group
import requests
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, status
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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

    def delete(self, request, food_pk, format=None):  # TODO verifier de ne pas supp celui dun autre
        object = self.get_object(food_pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticated])
class FoodList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        foods = Food.objects.filter(fridge=request.user)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(fridge=request.user)
            foods = Food.objects.filter(fridge=request.user)
            serializer2 = FoodSerializer(foods, many=True)
            return Response(serializer2.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class FoodDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        foods = Food.objects.filter(fridge=request.user)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        food = self.get_object(pk)
        serializer = FoodSerializer(food, data=request.data)
        if serializer.is_valid():
            serializer.save(fridge=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        food = self.get_object(pk)
        food.delete()
        foods = Food.objects.filter(fridge=request.user)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)
