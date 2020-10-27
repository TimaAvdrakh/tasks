from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model
from .models import Task, TaskChange, Notification
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password", )

class TaskSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        task = Task.objects.create(deadline = validated_data['deadline'],
                                   status = validated_data['status'],
                                   executor = validated_data['executor'],
                                   description = validated_data['description'],
                                   name= validated_data['name'])

        for watcher in validated_data['watchers']:
            task.watchers.set(watcher)
        task.save()
        return task

    class Meta:
        model = Task
        fields = ("id", 'name', 'description', 'status', 'executor', 'watchers', 'deadline', 'end_date')