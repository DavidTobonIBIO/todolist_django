from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm


def loginPage(request):
    """
    Handles user login functionality.
    
    - Renders the login page template for GET requests or failed logins.
    
    - If the user is already authenticated, redirects to the task-list page.
    
    - On POST requests, attempts to authenticate the user with the provided username and password.
        - If authentication is successful, logs the user in and redirects to the task-list page.
        - If authentication fails, displays appropriate error messages.
    
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: Redirects to the task-list page on successful login, or renders the login page with error messages.
    """
    
    if request.user.is_authenticated:
        return redirect("task-list")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("task-list")
        else:
            messages.error(request, "Username OR password are incorrect")
            
    return render(request, "users/login.html", {})

def registerPage(request):
    """
    Handles user registration requests.
    - Displays the registration form on GET requests.
    - Processes the registration form on POST requests.
        - If the form is valid, creates a new user, logs them in, and redirects to the task-list page.
        - If the form is invalid, displays an error message.
    - Renders the registration template with the form context.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered registration page or a redirect to the task-list page upon successful registration.
    """

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task-list")
        else:
            messages.error(request, "An error occurred during registration")
    
    # GET request
    form = UserRegisterForm()
    context = {"form": form}
    return render(request, "users/register.html", context)

def logoutUser(request):
    """
    Logs out the current user and redirects them to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect response to the login page.
    """
    
    logout(request)
    return redirect('login')