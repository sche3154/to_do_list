from django.db import models

# Create your models here.
# https://realpython.com/django-todo-lists/#demo
from django.utils import timezone

from django.db import models
from django.urls import reverse

def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

class ToDoList(models.Model):

    title = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("list", args =[self.id])

class ToDoItem(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    todo_list = models.ForeignKey(ToDoList, on_delete = models.CASCADE)

    def __str__(self):

        return "%s: due %s" % (self.title, self.due_date)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )
    
    class Meta:
        ordering = ["due_date"]