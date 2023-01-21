from django.urls import path

from todos.views import  TodoAPIView

urlpatterns = [
    path('', TodoAPIView.as_view(), name='create-todo'),

]