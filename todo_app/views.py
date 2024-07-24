from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ToDoList, ToDoItem
# Create your views here.

class ToDoListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return ToDoList.objects.filter(title__icontains=query)
        return ToDoList.objects.all()


class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_context_data(self):

        context = super().get_context_data()
    
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])

        return context
    
    def get_queryset(self):
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        return ToDoItem.objects.filter(todo_list = todo_list)

class ListCreate(CreateView):
    model = ToDoList
    template_name = "todo_app/todolist_form.html"
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context

    def get_success_url(self):
        return reverse("todo_app:list", args=[self.object.id])

class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("todo_app:list", args=[self.object.todo_list_id])

class ItemUpdate(UpdateView):
    model = ToDoItem
    template_name = "todo_app/todoitem_form.html"
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("todo_app:list", args=[self.object.todo_list_id])

class ListDelete(DeleteView):
    model = ToDoList

    success_url = reverse_lazy("todo_app:index")

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return reverse_lazy("list", args=[self.kwargs["list_id"]])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context



