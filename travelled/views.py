from django.shortcuts import render
from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from travel_checker_api.permissions import IsOwnerOrReadOnly
from .models import Travelled
from .serializers import TravelledSerializer

class TravelledList(generics.ListCreateAPIView):
    '''list places travelled and create a place travelled if logged in'''
    serializer_class = TravelledSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Travelled.objects.all()

    def perform_create(self, serializer):
        '''associate travelled with logged in user'''
        serializer.save(owner=self.request.user)

class TravelledDetail(generics.RetrieveUpdateDestroyAPIView):
    '''retrieve, edit,or delete if owned by user'''
    serializer_class = TravelledSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Travelled.objects.all()

    def delete(self, request, pk):
        page = self.get_object(pk)
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
