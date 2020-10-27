from django.db import models
from django.contrib.auth.models import User


class Status(models.TextChoices):
    PLANNING = 'PL', 'Planning'
    ACTIVE = 'AC', 'Active'
    CONTROLED = 'CL', 'Controled'
    ENDED = 'END', 'Ended'


class Task(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=100)
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    watchers = models.ManyToManyField(User, related_name='tasks_watchers')
    status = models.CharField(choices=Status.choices, default=Status.ACTIVE, max_length=3)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    deadline = models.DateField(null=False, blank=False)

    def __str__(self):
        return f"Task {self.name} created by  {self.executor.name}"

class TaskChange(models.Model):
    before = models.CharField(null=False, blank=False, max_length=100)
    after = models.CharField(null=False, blank=False, max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task {self.task.name} was changed from {self.before} to {self.after}"


class Notification(models.Model):
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = models.CharField(null=False, blank=False, max_length=100)
    users = models.ManyToManyField(User)

