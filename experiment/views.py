import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required



from .models import UserProfile

# Create your views here.

@login_required(login_url='sign-in')
def indexView(request):
    return render(request, 'index.html')

@login_required(login_url='sign-in')
def dashboardView(request):
    return render(request, 'dashboard.html')


def signInView(request):
    """
    Sign in view function.

    This function handles the sign in process for users. If the user is already authenticated,
    they will be redirected to the profile page. If the request method is POST, the function
    will attempt to authenticate the user with the provided username and password. If the
    authentication is successful, the user will be logged in and redirected to the profile
    page. Otherwise, an error message will be displayed and the user will be redirected back
    to the sign-in page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    """

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            name = User.objects.get(username=username).first_name
            user = authenticate(request, username=username, password=password)
        except:
            messages.error(request, f'User with this username does not exist')
            return redirect('sign-in')

        if user is not None:
            login(request, user)
            messages.success(request, f'Hi {name.title()}, welcome back!')
            return redirect('dashboard')

        else:
            messages.error(request, f'Invalid username or password. Try again.')
            return redirect('sign-in')

    return render(request, 'sign-in.html')

def signUpView(request):
    """
    View for user sign up.

    Args:
        request: The HTTP request object.

    Returns:
        If the user is authenticated, redirects to the dashboard.
        If the request method is POST:
            - If the user with the given email or username already exists, displays an error message and redirects to the registration page.
            - Otherwise, creates a new user with the provided email, password, first name, last name, and username.
        If the user is not authenticated and the request method is not POST, renders the 'sign-up.html' template.

    Side Effects:
        - Creates a new user in the database.
        - Creates a user profile for the new user.
        - Creates a directory for the new user in the 'data/users' directory.

    Raises:
        None.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')

        if User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
            messages.error(request, f'User with email {email} or username {username} already exists')
            return redirect('register')
        else:
            user = User.objects.create_user(
                email=email, password=password, first_name=first_name, last_name=last_name, username=username)

            user.save()
            UserProfile.objects.create(user=user)
            os.makedirs(f'data/users/{user.username}', exist_ok=True)
            messages.success(
                request, f'Account created for {first_name.title()}!')
            return redirect('sign-in')

    return render(request, 'sign-up.html')



def signOutView(request):
    """
    Signs out the current user.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: A redirect to the 'sign-in' page.
    """
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('sign-in')
