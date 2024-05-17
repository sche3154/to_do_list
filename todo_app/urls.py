# todo_list/todo_app/urls.py
from django.urls import path
from . import views

app_name = "todo_app"

urlpatterns = [
    path("",views.ToDoListView.as_view(),name="index"),
    path('list/<int:list_id>/', views.ItemListView.as_view(), name = "list"),
]