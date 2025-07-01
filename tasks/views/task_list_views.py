from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import TaskList
from django.contrib.auth.models import User


@login_required
def create_list(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            task_list = TaskList.objects.create(
                name=name, user=request.user
            )
            return redirect(f"/?list_id={task_list.id}")
        else:
            messages.error(request, "List name is required.")
            render(request, 'tasks/create_list.html')
            
    return render(request, 'tasks/create_list.html')


@login_required
def share_list(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id, user=request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            try:
                user = User.objects.get(username=username)
                if user != request.user:
                    if user not in task_list.shared_with.all():
                        task_list.shared_with.add(user)
                        messages.success(
                            request, f"List shared with {username} successfully!"
                        )
                    else:
                        messages.warning(request, f"List is already shared with {username}.")
                else:
                    messages.error(request, "You cannot share a list with yourself.")
            except User.DoesNotExist:
                messages.error(request, f'User "{username}" not found.')
        else:
            messages.error(request, "Username is required.")

    context = {
        'task_list': task_list,
        'shared_users': task_list.shared_with.all(),
    }
    return render(request, 'tasks/share_list.html', context)


@login_required
def unshare_list(request, list_id, user_id):
    try:
        task_list = get_object_or_404(TaskList, id=list_id)
        user_to_remove = get_object_or_404(User, id=user_id)
    except:
        return redirect('task-list')
            
    if user_to_remove in task_list.shared_with.all():
        task_list.shared_with.remove(user_to_remove)
        
    else:
        messages.error(request, "User is not shared with this list.")
    
    if task_list.user == request.user:
        return redirect('share-list', list_id=list_id)
    else:
        return redirect('task-list')


@login_required
def delete_list(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id)

    if task_list.user != request.user:
        messages.error(request, "You don't have permission to delete this list.")
        return redirect("task-list")

    task_list.delete()

    return redirect("task-list")
