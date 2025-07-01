from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task-list"),
    path("completed/", views.completed_tasks, name="completed-tasks"),
    path("create/", views.create_task, name="create-task"),
    path("edit/<int:pk>/", views.edit_task, name="edit-task"),
    path("delete/<int:pk>/", views.delete_task, name='delete-task'),
    path("toggle/<int:pk>/", views.toggle_complete, name="toggle-complete"),    
]