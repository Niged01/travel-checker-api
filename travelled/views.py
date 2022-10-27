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
    queryset = Travelled.objects.annotate(
        comments_count=Count(
            'comment', distinct=True
        ),
        likes_count=Count('like', distinct=True),
    ).order_by('-date_created')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'like__owner__profile',
        'owner__profile',
        'owner__followed__owner__profile',
    ]
    search_fields = [
        'owner__username',
        'content',
        'title',
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
    ]

    def perform_create(self, serializer):
        '''associate travelled with logged in user'''
        serializer.save(owner=self.request.user)

class TravelledDetail(generics.RetrieveUpdateDestroyAPIView):
    '''retrieve, edit,or delete if owned by user'''
    serializer_class = TravelledSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Travelled.objects.annotate(
        comments_count=Count(
            'comments', distinct=True
        ),
        likes_count=Count('like', distinct=True),
    ).order_by('-date_created') 

