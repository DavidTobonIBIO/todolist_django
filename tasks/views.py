from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, TaskList
from .forms import TaskForm


@login_required
def task_list(request):
    tasks = Task.objects.filter(Q(user=request.user), Q(completed=False)).order_by(
        "due_date", "-priority"
    )

    context = {"page_title": "My Tasks", "tasks": tasks}
    return render(request, "tasks/task_list.html", context)


@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(Q(user=request.user), Q(completed=True))

    context = {"page_title": "Completed Tasks", "tasks": tasks}
    return render(request, "tasks/task_list.html", context)


@login_required
def create_task(request):
    if request.method == "POST":
        task_list_name = request.POST.get("task_list_name")
        if task_list_name == '':
            task_list_name = "My Tasks"
        task_list, created = TaskList.objects.get_or_create(name=task_list_name, user=request.user)

        Task.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            due_date=request.POST.get("due_date"),
            priority=request.POST.get("priority"),
            task_list=task_list,
        )

        return redirect("task-list")

    form = TaskForm()
    task_lists = TaskList.objects.filter(user=request.user)
    context = {"form": form, "task_lists": task_lists, "action": "create"}
    return render(request, "tasks/task_form.html", context)


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == "POST":
        task_list_name = request.POST.get("task_list_name")
        task_list, created = TaskList.objects.get_or_create(name=task_list_name, user=request.user)

        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.due_date = request.POST.get("due_date")
        task.priority = request.POST.get("priority")

        task.task_list = task_list

        task.save()
        if task.completed:
            return redirect("completed-tasks")
        return redirect("task-list")

    form = TaskForm(instance=task)
    task_lists = TaskList.objects.filter(user=request.user)
    context = {"form": form, "task": task, "task_lists": task_lists, "action": "edit"}
    print(task.task_list.name)
    return render(request, "tasks/task_form.html", context)


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        completed = task.completed
        task.delete()
        if task.completed:
            return redirect("completed-tasks")
        return redirect("task-list")

    context = {"task": task}
    return render(request, "tasks/task_delete.html", context)


@login_required
def toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    previous_state = task.completed
    task.completed = not task.completed
    task.save()

    status = "completed" if task.completed else "reopened"
    # messages.success(request, f'Task "{task.title}" {status}!')
    if previous_state == True:
        # if the task was completed before changing state, then redirect to the view where it was located before state change
        return redirect("completed-tasks")
    return redirect("task-list")
