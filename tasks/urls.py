from django.urls import path
from .views import task_views, task_list_views

urlpatterns = [
    path("", task_views.task_list, name="task-list"),
    path("completed/", task_views.completed_tasks, name="completed-tasks"),
    path("create/", task_views.create_task, name="create-task"),
    path("edit/<int:pk>/", task_views.edit_task, name="edit-task"),
    path("delete/<int:pk>/", task_views.delete_task, name="delete-task"),
    path("toggle/<int:pk>/", task_views.toggle_complete, name="toggle-complete"),
    path("lists/create/", task_list_views.create_list, name="create-list"),
    path("lists/delete/<int:list_id>/", task_list_views.delete_list, name="delete-list"),
    path("lists/share/<int:list_id>/", task_list_views.share_list, name="share-list"),
    path(
        "lists/unshare/<int:list_id>/user/<int:user_id>/",
        task_list_views.unshare_list,
        name="unshare-list",
    ),
]
