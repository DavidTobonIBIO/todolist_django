from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import TaskList
from django.contrib.auth.models import User

@login_required
def create_list(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        
        if name:
            TaskList.objects.create(
                name=name,
                description=description,
                user=request.user
            )
            messages.success(request, f'List "{name}" created successfully!')
        else:
            messages.error(request, "List name is required.")
    
    return redirect("task-list")


@login_required
def share_list(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id, user=request.user)
    
    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            try:
                user = User.objects.get(username=username)
                if user != request.user:
                    task_list.shared_with.add(user)
                    messages.success(request, f'List shared with {username} successfully!')
                else:
                    messages.error(request, "You cannot share a list with yourself.")
            except User.DoesNotExist:
                messages.error(request, f'User "{username}" not found.')
        else:
            messages.error(request, "Username is required.")
    
    return redirect("task-list")


@login_required  
def unshare_list(request, list_id, user_id):
    task_list = get_object_or_404(TaskList, id=list_id, user=request.user)
    user = get_object_or_404(User, id=user_id)
    
    task_list.shared_with.remove(user)
    messages.success(request, f'List no longer shared with {user.username}.')
    
    return redirect("task-list")