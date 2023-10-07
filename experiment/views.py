import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from django.urls import reverse_lazy

from django.forms.models import BaseModelForm
from .forms import InventoryForm, ItemForm, SupplierForm





from .models import UserProfile, Inventory

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


# defining inventoryView, addInventoryView, updateInventoryView for inventory page 

class inventoryView(LoginRequiredMixin,ListView):

    login_url = 'sign-in'
    model = Inventory
    template_name = 'inventory.html'
    queryset = Inventory.objects.filter(completed=False)
    context_object_name = 'inventory_list'

class addInventoryView(LoginRequiredMixin,CreateView):
    login_url = 'sign-in'
    model = Inventory
    template_name = 'add-inventory.html'
    success_url = reverse_lazy('inventory')
    form_class = InventoryForm

    """
    Get the context data for the view.

    :param kwargs: Additional keyword arguments to pass to the superclass method.
    :return: The context data containing the 'items' and 'measurement_units'.
    """

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        messages.success(self.request, 'Inventory added successfully')
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)


class updateInventoryView(LoginRequiredMixin,UpdateView):
    login_url = 'sign-in'
    model = Inventory
    template_name = 'update-inventory.html'
    form_class = InventoryForm
    success_url = reverse_lazy('inventory')

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'save-as-new':
            new_instance = form.save(commit=False)
            new_instance.id = None
            new_instance.added_by = self.request.user
            new_instance.save()
            # Add success message
            messages.success(self.request, 'Saved as new successfully.')
            return super().form_valid(form)
        elif action == 'update':
            # Add success message
            messages.success(self.request, 'Update successful.')
            return super().form_valid(form)

@login_required(login_url = 'sign-in')
def markascomplete(request, pk):
    inventory = Inventory.objects.get(id=pk)
    inventory.completed = True
    inventory.save()
    messages.success(
        request, f'{inventory.item.name} {inventory.batch} marked as complete')
    return redirect('inventory')

@login_required(login_url = 'sign-in')
def addItemView(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.added_by = request.user
            form_instance.save()
            form.save()
            messages.success(request, 'Item added successfully')
            return redirect('add-inventory')
    context = {
        'form': form,
    }
    return render(request, 'add-item.html', context)

@login_required(login_url = 'sign-in')
def addSupplierView(request):
    form = SupplierForm()
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.added_by = request.user
            form_instance.save()
            messages.success(request, 'Supplier added successfully')
            return redirect('add-item')
    context = {
        'form': form,
    }
    return render(request, 'add-supplier.html', context)
