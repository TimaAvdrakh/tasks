from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
     path('user/create/', CreateUserView.as_view()),
     path('my_tasks/', TaskList.as_view()),
     path('task/detail/{pk}', TaskDetail.as_view())
]



