from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from ..models import Task, TaskList
from ..forms import TaskForm
from django.db.models import Q


@login_required
def task_list(request):
    selected_list_id = request.GET.get("list_id", "all")

    if selected_list_id == "all":
        # all tasks the user has access to
        tasks = Task.objects.filter(
            Q(user=request.user) | Q(task_list__shared_with=request.user) | Q(task_list__user=request.user)
        ).filter(completed=False)
        selected_list = None
    else:
        try:
            selected_list = TaskList.objects.get(
                Q(id=selected_list_id),
                Q(user=request.user) | Q(shared_with=request.user),
            )
            tasks = Task.objects.filter(task_list=selected_list, completed=False)
        except TaskList.DoesNotExist:
            messages.error(request, "List not found or you don't have access.")
            return redirect("task-list")

    tasks = tasks.order_by("due_date", "-priority")

    owned_lists = TaskList.objects.filter(user=request.user)
    shared_lists = TaskList.objects.filter(shared_with=request.user)

    context = {
        "page_title": "My Tasks",
        "tasks": tasks,
        "owned_lists": owned_lists,
        "shared_lists": shared_lists,
        "selected_list": selected_list,
        "selected_list_id": selected_list_id,
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def completed_tasks(request):
    selected_list_id = request.GET.get("list_id", "all")

    if selected_list_id == "all":
        tasks = Task.objects.filter(
            Q(completed=True),
            Q(user=request.user) | Q(task_list__shared_with=request.user),
        )
        selected_list = None
    else:
        try:
            selected_list = TaskList.objects.get(
                Q(id=selected_list_id),
                Q(user=request.user) | Q(shared_with=request.user),
            )
            tasks = Task.objects.filter(task_list=selected_list, completed=True)
        except TaskList.DoesNotExist:
            messages.error(request, "List not found or you don't have access.")
            return redirect("completed-tasks")

    tasks = tasks.order_by("-completed_at")

    owned_lists = TaskList.objects.filter(user=request.user)
    shared_lists = TaskList.objects.filter(shared_with=request.user)

    context = {
        "page_title": "Completed Tasks",
        "tasks": tasks,
        "owned_lists": owned_lists,
        "shared_lists": shared_lists,
        "selected_list": selected_list,
        "selected_list_id": selected_list_id,
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def create_task(request):
    selected_list_id = request.GET.get("list_id")

    if request.method == "POST":
        task_list_name = request.POST.get("task_list_name")
        
        # default task list name of user didnt provide info
        if task_list_name == "":
            task_list_name = "My Tasks"
        
        try:
            task_list = TaskList.objects.get(
                Q(name=task_list_name), Q(user=request.user) | Q(shared_with=request.user)
            )

        except TaskList.DoesNotExist:
            # create default list
            task_list = TaskList.objects.create(
                user=request.user,
                name=task_list_name,
            )

        Task.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            due_date=request.POST.get("due_date"),
            priority=request.POST.get("priority"),
            task_list=task_list,
        )

        if selected_list_id:
            return redirect(f"/?list_id={selected_list_id}")
        return redirect("task-list")

    all_lists = TaskList.objects.filter(
        Q(user=request.user) | Q(shared_with=request.user)
    ).order_by("name")

    # selected_list used when coming from a view of an specific list
    selected_list = None
    if selected_list_id:
        try:
            selected_list = TaskList.objects.get(
                Q(id=selected_list_id),
                Q(user=request.user) | Q(shared_with=request.user),
            )
        except TaskList.DoesNotExist:
            pass

    form = TaskForm()

    context = {
        "form": form,
        "task_lists": all_lists,
        "action": "create",
        "selected_list": selected_list,
    }
    return render(request, "tasks/task_form.html", context)


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Check if user has permission (task owner, list owner, or shared user)
    if not (
        task.user == request.user
        or request.user in task.task_list.shared_with.all()
        or task.task_list.user == request.user
    ):
        messages.error(request, "You don't have permission to edit this task.")
        return redirect("task-list")

    if request.method == "POST":
        # only list owner can change task list
        if task.task_list.user == request.user:
            task_list_name = request.POST.get("task_list_name")
            task_list, created = TaskList.objects.get_or_create(
                name=task_list_name, user=request.user
            )
            task.task_list = task_list

        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.due_date = request.POST.get("due_date")
        task.priority = request.POST.get("priority")
        task.save()

        return redirect("task-list")

    form = TaskForm(instance=task)

    all_lists = TaskList.objects.filter(
        Q(user=request.user) | Q(shared_with=request.user)
    ).order_by("name")

    context = {"form": form, "task": task, "task_lists": all_lists, "action": "edit"}
    return render(request, "tasks/task_form.html", context)


@login_required
def delete_task(request, pk):
    task = None
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return redirect("task-list")
        
    # only task creator or list owner can delete tasks
    if not (task.user == request.user or task.task_list.user == request.user):
        messages.error(request, "You don't have permission to delete this task.")
        return redirect("task-list")

    was_completed = task.completed
    task.delete()

    if was_completed:
        return redirect("completed-tasks")
    return redirect("task-list")


@login_required
def toggle_complete(request, pk):
    task = None
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": True,
                    "completed": False,
                    "task_id": 0,
                }
            )

    if not (
        task.user == request.user
        or request.user in task.task_list.shared_with.all()
        or task.task_list.user == request.user
    ):

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "success": False,
                    "error": "You don't have permission to modify this task.",
                },
                status=403,
            )
        else:
            messages.error(request, "You don't have permission to modify this task.")
            return redirect("task-list")

    previous_state = task.completed
    task.completed = not task.completed
    task.save()

    # AJAX requests
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "completed": task.completed,
                "task_id": task.pk,
            }
        )

    # handle regular requests with page reload
    if previous_state == True:
        return redirect("completed-tasks")
    return redirect("task-list")
