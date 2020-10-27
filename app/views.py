from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model # If used custom user model
from .models import Task, TaskChange, Notification
from .serializers import UserSerializer, TaskSerializer
from django.db.models import Q
from django.http import Http404
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

from rest_framework import status



from rest_framework import viewsets


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.IsAuthenticated # Or anon users can't register
    ]
    serializer_class = UserSerializer


class TaskListView(ListAPIView):
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self, request):
        user = request.user
        q = self.queryset.filter(Q(executor=user) | Q(watcher=user))
        return q

class TaskDetail(APIView):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = permissions.IsAuthenticated

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return task(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        status = request.date['status']
        user = request.user

        if request.user != task.executor:
            return Response({'detail': 'U are not allowed to edit'}, status=status.HTTP_400_BAD_REQUEST)

        notification = Notification(task=task, content="Task Status Has Changed", users=task.watchers)
        notification.save()
        # before
        # after
        # task
        # changed_by

        tk = TaskChange(before=task.status , after=status, task=task, changed_by=task)
        tk.save()

        task.status = status
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyTasks(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def gueryset(self, request, **kwargs):

        user = request.user
        q = self.queryset.filter(Q(watchers=user) | Q(executor=user))
        return q

class TaskList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *arg, **kwargs):
        user = request.user
        q = self.queryset.filter(Q(watchers=user) | Q(executor=user))
        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)