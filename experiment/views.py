import os
from typing import Any
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
from .forms import InventoryForm, ItemForm, SupplierForm, SpinProgramForm, SpinStepForm, AddStackForm, ProjectForm, ExperimentForm, UserProfileForm

from django.conf import settings


from .models import UserProfile, Inventory, MeasurementUnit, Formulation, IngredientQuantity, Layer, SpinCoatingCondition, SpinProgram, SpinStep, ThermalEvaporationCondition, Stack, StackLayerRelationShip, Project

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
            messages.error(
                request, f'Invalid username or password. Try again.')
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
            messages.error(
                request, f'User with email {email} or username {username} already exists')
            return redirect('sign-up')
        else:
            user = User.objects.create_user(
                email=email, password=password, first_name=first_name, last_name=last_name, username=username)

            user.save()
            UserProfile.objects.create(user=user)
            absolute_path = os.path.join(
                settings.MEDIA_ROOT, 'users', user.username)
            os.makedirs(absolute_path, exist_ok=True)

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


@login_required(login_url='sign-in')
def profileView(request):
    user = request.user
    projects = Project.objects.filter(author=user)

    context = {
        'user': user,
        'projects': projects,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='sign-in')
def updateUserProfileView(request):
    user = request.user
    profile = user.userprofile
    form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            messages.success(request, 'Profile updated successfully')
            return redirect('profile')

    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'update-profile.html', context)


@login_required(login_url='sign-in')
def addProjectView(request):

    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        form.instance.author = User.objects.get(
            username=request.user.username)

        if form.is_valid():

            form.save()
            messages.success(request, 'Project added successfully')
            return redirect('profile')

    context = {

        'form': form,

    }
    return render(request, 'add-project.html', context)


@login_required(login_url='sign-in')
def updateProjectView(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully')
            return redirect('profile')
    context = {
        'form': form
    }
    return render(request, 'update-project.html', context)


@login_required(login_url='sign-in')
def addExperimentView(request, pk):
    project = Project.objects.get(id=pk)
    form = ExperimentForm()
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            form.instance.author = User.objects.get(
                username=request.user.username
            )

            form.instance.project = project
            form.save()
            messages.success(request, 'Experiment added successfully')
            return redirect('profile')

    context = {
        'form': form,
        'project': project
    }

    return render(request, 'add-experiment.html', context)


# defining inventoryView, addInventoryView, updateInventoryView for inventory page

class inventoryView(LoginRequiredMixin, ListView):

    login_url = 'sign-in'
    model = Inventory
    template_name = 'inventory.html'
    queryset = Inventory.objects.filter(completed=False)
    context_object_name = 'inventory_list'


class addInventoryView(LoginRequiredMixin, CreateView):
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


class updateInventoryView(LoginRequiredMixin, UpdateView):
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


@login_required(login_url='sign-in')
def markascomplete(request, pk):
    inventory = Inventory.objects.get(id=pk)
    inventory.completed = True
    inventory.save()
    messages.success(
        request, f'{inventory.item.name} {inventory.batch} marked as complete')
    return redirect('inventory')


@login_required(login_url='sign-in')
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


@login_required(login_url='sign-in')
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


# formulation page views
@login_required(login_url='sign-in')
def formulationView(request):
    formulation_list = Formulation.objects.filter(completed=False)
    ingredient_quantity = IngredientQuantity.objects.all()

    context = {
        'formulation_list': formulation_list,
        'IngredientQuantity': ingredient_quantity,
    }

    return render(request, 'formulation.html', context)
# class formulationView(LoginRequiredMixin,ListView):
#     login_url = 'sign-in'
#     model = Formulation
#     template_name = 'formulation.html'
#     queryset = Formulation.objects.filter(completed=False)
#     context_object_name = 'formulation_list'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['IngredientQuantity'] = IngredientQuantity.objects.all()
#         return context


@login_required(login_url='sign-in')
def addformulationView(request):

    if request.method == 'POST':
        added_by = request.user
        name = request.POST.get('formulation-name')
        atmosphere = request.POST.get('atmosphere')

        created = request.POST.get('formulation-created')
        notes = request.POST.get('notes')

        formulation = Formulation.objects.create(added_by=added_by,
                                                 name=name, atmosphere=atmosphere, notes=notes, created=created)

        inventory_ids = request.POST.getlist('inventory-name[]')
        quantities = request.POST.getlist('quantity[]')
        measurement_units_ids = request.POST.getlist('measurement-unit[]')

        for i in range(len(inventory_ids)):
            IngredientQuantity.objects.create(added_by=added_by, formulation=formulation, inventory=Inventory.objects.get(
                id=inventory_ids[i]), quantity=quantities[i], measurement_unit=MeasurementUnit.objects.get(id=measurement_units_ids[i]))

        messages.success(request, 'Formulation added successfully')
        return redirect('formulation')

    inventory_list = Inventory.objects.filter(
        completed=False, item__category__name='Chemical')
    measurement_units = MeasurementUnit.objects.all()
    context = {'inventory_list': inventory_list, 'measurement_units': measurement_units,
               }
    return render(request, 'add-formulation.html', context)


@login_required(login_url='sign-in')
def updateformulationView(request, pk):
    formulation = Formulation.objects.get(id=pk)
    ingredients = IngredientQuantity.objects.filter(
        formulation=formulation)
    inventory_list = Inventory.objects.filter(
        completed=False, item__category__name='Chemical')
    measurement_units = MeasurementUnit.objects.all()

    added_by = request.user
    name = request.POST.get('formulation-name')
    atmosphere = request.POST.get('atmosphere')
    created = request.POST.get('formulation-created')
    notes = request.POST.get('notes')

    inventory_ids = request.POST.getlist('inventory-name[]')
    quantities = request.POST.getlist('quantity[]')
    measurement_units_ids = request.POST.getlist('measurement-unit[]')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save-as-new':
            new_formulation = Formulation.objects.create(added_by=added_by,
                                                         name=name, atmosphere=atmosphere, notes=notes, created=created)

            for i in range(len(inventory_ids)):
                IngredientQuantity.objects.create(added_by=added_by, formulation=new_formulation, inventory=Inventory.objects.get(
                    id=inventory_ids[i]), quantity=quantities[i], measurement_unit=MeasurementUnit.objects.get(id=measurement_units_ids[i]))
            messages.success(request, 'New Formulation has been added')
            return redirect('formulation')
        elif action == 'update':
            formulation.name = name
            formulation.atmosphere = atmosphere
            formulation.notes = notes
            formulation.save()
            if len(ingredients) == len(inventory_ids):
                for count, ingredient in enumerate(ingredients):
                    ingredient.inventory = Inventory.objects.get(
                        id=inventory_ids[count])
                    ingredient.quantity = quantities[count]
                    ingredient.measurement_unit = MeasurementUnit.objects.get(
                        id=measurement_units_ids[count])
                    ingredient.save()
            # what if user adds more ingredients to the forumulation
            elif len(ingredients) < len(inventory_ids):
                # save the existing ingredients
                for count, ingredient in enumerate(ingredients):
                    ingredient.inventory = Inventory.objects.get(
                        id=inventory_ids[count])
                    ingredient.quantity = quantities[count]
                    ingredient.measurement_unit = MeasurementUnit.objects.get(
                        id=measurement_units_ids[count])
                    ingredient.save()
                for i in range(len(ingredients), len(inventory_ids)):  # add the new ingredients
                    IngredientQuantity.objects.create(added_by=added_by, formulation=formulation, inventory=Inventory.objects.get(
                        id=inventory_ids[i]), quantity=quantities[i], measurement_unit=MeasurementUnit.objects.get(id=measurement_units_ids[i]))

            # what if user removes ingredients from the formulation

            elif len(ingredients) > len(inventory_ids):
                for i, ingredient in enumerate(ingredients):
                    if i < len(inventory_ids):
                        ingredient.inventory = Inventory.objects.get(
                            id=inventory_ids[i])
                        ingredient.quantity = quantities[i]
                        ingredient.measurement_unit = MeasurementUnit.objects.get(
                            id=measurement_units_ids[i])
                        ingredient.save()
                    elif i >= len(inventory_ids):
                        ingredient.delete()

            else:
                messages.error(
                    request, 'Formulation ingredients could not be updated')
        messages.success(request, 'Formulation updated successfully')

        return redirect('formulation')

    context = {'formulation': formulation,
               'ingredients': ingredients, 'inventory_list': inventory_list, 'measurement_units': measurement_units, }
    return render(request, 'update-formulation.html', context)


# layer page views

@login_required(login_url='sign-in')
def layerRouter(request, pk):
    layer = Layer.objects.get(id=pk)

    if layer.coating_method == 'Spin Coating':
        return redirect('update-spin-coated-layer', pk)
    elif layer.coating_method == 'Thermal Evaporation':
        return redirect('update-thermal-evaporated-layer', pk)


class LayerView(LoginRequiredMixin, ListView):
    login_url = 'sign-in'
    model = Layer
    template_name = 'layer.html'
    queryset = Layer.objects.all()
    context_object_name = 'layer_list'


@login_required(login_url='sign-in')
def addSpinCoatedLayer(request):

    if request.method == 'POST':
        layer_type = request.POST.get('layer-type')
        name = request.POST.get('name')
        formulation = request.POST.get('formulation')
        program = request.POST.get('program-id')
        formulation_volume = request.POST.get('formulation-volume')

        antisolvent_used = request.POST.get('antisolvent-used')
        antisolvent = request.POST.get('antisolvent')
        antisolvent_volume = request.POST.get('antisolvent-volume')
        antisolvent_drop_time = request.POST.get('antisolvent-drop-time')

        room_temperature = request.POST.get('room-temperature')
        room_humidity = request.POST.get('room-humidity')
        atmosphere = request.POST.get('atmosphere')

        drying_type = request.POST.get('drying-type')
        drying_temperature = request.POST.get('drying-temperature')
        drying_time = request.POST.get('drying-time')

        created = request.POST.get('created')

        layer = Layer.objects.create(added_by=request.user, name=name, coating_method='Spin Coating', layer_type=layer_type,
                                     formulation=Formulation.objects.get(id=formulation), created=created)

        if antisolvent_used == 'True':
            antisolvent_used = True

            SpinCoatingCondition.objects.create(added_by=request.user, layer=layer,
                                                program=SpinProgram.objects.get(id=program), formulation_volume=formulation_volume,
                                                antisolvent_used=antisolvent_used, antisolvent=Inventory.objects.get(
                                                    id=antisolvent),
                                                antisolvent_volume=antisolvent_volume, antisolvent_drop_time=antisolvent_drop_time,
                                                room_temperature=room_temperature, room_humidity=room_humidity, atmosphere=atmosphere,
                                                drying_type=drying_type, drying_temperature=drying_temperature,
                                                drying_time=drying_time)

        else:
            antisolvent_used = False
            SpinCoatingCondition.objects.create(added_by=request.user, layer=layer,
                                                program=SpinProgram.objects.get(id=program), formulation_volume=formulation_volume,
                                                antisolvent_used=antisolvent_used,
                                                room_temperature=room_temperature, room_humidity=room_humidity, atmosphere=atmosphere,
                                                drying_type=drying_type, drying_temperature=drying_temperature,
                                                drying_time=drying_time)

        messages.success(request, 'Layer added successfully')
        return redirect('layer')
    programs = SpinProgram.objects.all()
    formulations = Formulation.objects.filter(completed=False)
    inventory_list = Inventory.objects.filter(
        item__type='Liquid', completed=False)

    context = {'programs': programs,
               'formulations': formulations, 'inventory_list': inventory_list}

    return render(request, 'add-spin-coated-layer.html', context)


@login_required(login_url='sign-in')
def updateSpinCoatedLayer(request, pk):
    # values for context
    layer = Layer.objects.get(id=pk)
    condition = SpinCoatingCondition.objects.get(layer=layer)
    programs = SpinProgram.objects.all()
    formulations = Formulation.objects.filter(completed=False)
    inventory_list = Inventory.objects.filter(
        item__type='Liquid', completed=False)

    if condition.antisolvent_used == True:
        antisolvent_used = 'Yes'
    else:
        antisolvent_used = 'No'

    if request.method == 'POST':

        # getting ation value for save as new or update
        action = request.POST.get('action')

        # values for update or save as new
        layer_type = request.POST.get('layer-type')
        name = request.POST.get('name')
        formulation = request.POST.get('formulation')
        program = request.POST.get('program-id')
        formulation_volume = request.POST.get('formulation-volume')

        antisolvent__used = request.POST.get('antisolvent-used')
        antisolvent = request.POST.get('antisolvent')
        antisolvent_volume = request.POST.get('antisolvent-volume')
        antisolvent_drop_time = request.POST.get('antisolvent-drop-time')

        room_temperature = request.POST.get('room-temperature')
        room_humidity = request.POST.get('room-humidity')
        atmosphere = request.POST.get('atmosphere')

        drying_type = request.POST.get('drying-type')
        drying_temperature = request.POST.get('drying-temperature')
        drying_time = request.POST.get('drying-time')

        created = request.POST.get('created')

        if action == 'save-as-new':

            layer = Layer.objects.create(added_by=request.user, name=name, coating_method='Spin Coating',
                                         layer_type=layer_type, formulation=Formulation.objects.get(
                                             id=formulation),
                                         created=created)

            if antisolvent__used == 'True':
                antisolvent__used = True

                SpinCoatingCondition.objects.create(added_by=request.user, layer=layer,
                                                    program=SpinProgram.objects.get(id=program), formulation_volume=formulation_volume,
                                                    antisolvent_used=antisolvent__used, antisolvent=Inventory.objects.get(
                                                        id=antisolvent),
                                                    antisolvent_volume=antisolvent_volume, antisolvent_drop_time=antisolvent_drop_time,
                                                    room_temperature=room_temperature, room_humidity=room_humidity, atmosphere=atmosphere,
                                                    drying_type=drying_type, drying_temperature=drying_temperature,
                                                    drying_time=drying_time)

            else:
                antisolvent__used = False
                SpinCoatingCondition.objects.create(added_by=request.user, layer=layer,
                                                    program=SpinProgram.objects.get(id=program), formulation_volume=formulation_volume,
                                                    antisolvent_used=antisolvent__used,
                                                    room_temperature=room_temperature, room_humidity=room_humidity, atmosphere=atmosphere,
                                                    drying_type=drying_type, drying_temperature=drying_temperature,
                                                    drying_time=drying_time)

            messages.success(request, f'{name} layer added successfully')

            return redirect('layer')

        elif action == 'update':

            try:
                layer.layer_type = layer_type
                layer.name = name
                layer.formulation = Formulation.objects.get(id=formulation)
                layer.created = created

                condition.program = SpinProgram.objects.get(id=program)
                condition.formulation_volume = formulation_volume
                condition.antisolvent_used = antisolvent__used
                if condition.antisolvent_used == True:
                    condition.antisolvent = Inventory.objects.get(
                        id=antisolvent)
                    condition.antisolvent_volume = antisolvent_volume
                    condition.antisolvent_drop_time = antisolvent_drop_time
                condition.room_temperature = room_temperature
                condition.room_humidity = room_humidity
                condition.atmosphere = atmosphere
                condition.drying_type = drying_type
                condition.drying_temperature = drying_temperature
                condition.drying_time = drying_time
                layer.save()
                condition.save()
                messages.success(request, f'{name} layer updated successfully')
            except:
                messages.error(request, 'Layer could not be updated')

            return redirect('layer')

    context = {'layer': layer, 'programs': programs,
               'formulations': formulations, 'inventory_list': inventory_list, 'antisolvent_used': antisolvent_used, 'condition': condition}
    return render(request, 'update-spin-coated-layer.html', context)


@login_required(login_url='sign-in')
def addSpinStep(request):

    form = SpinStepForm()

    if request.method == 'POST':
        form = SpinStepForm(request.POST)
        if SpinStep.objects.filter(spin_speed=request.POST.get('spin_speed'), spin_time=request.POST.get('spin_time'), spin_acceleration=request.POST.get('spin_acceleration')).exists():
            messages.error(
                request, 'Spin step already exists, please use the existing spin step')
        elif form.is_valid():
            form.save()
            return redirect('add-spin-program')

    context = {'form': form}
    return render(request, 'spin-step.html', context)


@login_required(login_url='sign-in')
def addSpinProgram(request):

    form = SpinProgramForm()
    if request.method == 'POST':
        form = SpinProgramForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('add-spin-coated-layer')

    context = {'form': form}
    return render(request, 'spin-program.html', context)


def addThermalEvaporatedLayerView(request):
    formulation_list = Formulation.objects.filter(completed=False)
    context = {'formulation_list': formulation_list}
    if request.method == 'POST':
        layer_type = request.POST.get('layer-type')
        name = request.POST.get('name')
        formulation = request.POST.get('formulation')
        pressure = request.POST.get('pressure')
        created = request.POST.get('created')
        layer = Layer.objects.create(added_by=request.user, name=name, coating_method='Thermal Evaporation', layer_type=layer_type,
                                     formulation=Formulation.objects.get(id=formulation), created=created)

        ThermalEvaporationCondition.objects.create(
            added_by=request.user, layer=layer, pressure=pressure)

        messages.success(request, 'Layer added successfully')
        return redirect('layer')

    return render(request, 'add-thermal-evaporated-layer.html', context)


def updateThermalEvaporatedLayerView(request, pk):
    layer = Layer.objects.get(id=pk)
    condition = ThermalEvaporationCondition.objects.get(layer=layer)
    if request.method == 'POST':
        layer.layer_type = request.POST.get('layer-type')
        layer.name = request.POST.get('name')
        layer.formulation = Formulation.objects.get(
            id=request.POST.get('formulation'))
        layer.created = request.POST.get('created')
        layer.save()
        condition.pressure = request.POST.get('pressure')
        condition.save()
        messages.success(request, 'Layer updated successfully')
        return redirect('layer')
    context = {'layer': layer, 'condition': condition}
    return render(request, 'update-thermal-evaporated-layer.html', context)


def StackView(request):
    stack_list = Stack.objects.all()
    related_stacks = StackLayerRelationShip.objects.all()

    context = {
        'object_list': stack_list,  # ListView expects 'object_list' by default
        'related_stacks': related_stacks,
    }

    return render(request, 'stack.html', context)

# class StackView(LoginRequiredMixin,ListView):
#     login_url = 'sign-in'
#     model = Stack
#     template_name = 'stack.html'


#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         stack_list = Stack.objects.all()

#         kwargs['stack_list'] = stack_list
#         kwargs['realted_stacks'] = StackLayerRelationShip.objects.all()


#         return super().get_context_data(**kwargs)

@login_required(login_url='sign-in')
def addStackView(request):

    layer_list = Layer.objects.all()
    form = AddStackForm
    if request.method == 'POST':
        selected_layers = request.POST.get("selected-layers")
        selected_layers_list = selected_layers.split(
            ",")     # Split the selected values into a list
        form = AddStackForm(request.POST)
        if form.is_valid():
            form.instance.added_by = request.user
            form_instance = form.save(commit=False)
            form.save()

            for layer in selected_layers_list:
                StackLayerRelationShip.objects.create(
                    stack=form_instance, layer=Layer.objects.get(id=layer))

            messages.success(request, 'Stack added successfully')
            return redirect('stack')
        else:
            messages.error(request, 'Stack could not be added')

    context = {'layer_list': layer_list, 'form': form}
    return render(request, 'add-stack.html', context)


@login_required(login_url='sign-in')
def updateStackView(request, pk):
    stack = Stack.objects.get(id=pk)
    substrate = Inventory.objects.get(id=stack.substrate.id)
    layers = stack.layers.all().order_by('-stacklayerrelationship__added_at')
    layer_list = Layer.objects.all()
    form = AddStackForm(instance=stack)
    selectedValues = [
        i.id for i in stack.layers.all().order_by('stacklayerrelationship__added_at')]
    selectedValues = ','.join([str(i) for i in selectedValues])

    if request.method == 'POST':
        form = AddStackForm(request.POST, instance=stack)

        if form.is_valid():

            selected_layers = request.POST.get("selected-layers")
            selected_layers_list = selected_layers.split(
                ",")
            form.instance.added_by = request.user
            form_instance = form.save(commit=False)
            form.save()

            for layer in StackLayerRelationShip.objects.filter(stack=stack):
                layer.delete()
            for layer in selected_layers_list:
                StackLayerRelationShip.objects.create(
                    stack=form_instance, layer=Layer.objects.get(id=layer))
            messages.success(request, 'Stack updated successfully')
            return redirect('stack')
        else:

            messages.error(request, 'Stack could not be updated')

    context = {'form': form,
               'substrate': substrate, 'stack': stack,
               'layers': layers, 'selectedValues': selectedValues, 'layer_list': layer_list}

    return render(request, 'update-stack.html', context)
