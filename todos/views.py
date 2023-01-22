from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from todos.models import Todo
from todos.serializers import TodoSerializer


class TodoAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'title', 'desc', 'is_complete']
    search_fields = ['id', 'title', 'desc', 'is_complete']
    ordering_fields = ['id', 'title', 'desc', 'is_complete']


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
