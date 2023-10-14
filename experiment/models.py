import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.
def user_profile_path(instance, filename):
    """
    Generate the user profile path for a given filename.

    Args:
        instance (UserProfile): The UserProfile instance.
        filename (str): The name of the file.

    Returns:
        str: The path of the user's profile file.
    """
    username = instance.user.username
    ext = filename.split('.')[-1]

    # If a file with the same name exists, delete it
    try:
        old_file = UserProfile.objects.get(pk=instance.pk).profile_picture
        if old_file:
            # Delete the old file if it exists
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except UserProfile.DoesNotExist:
        pass

    return os.path.join('users', username, 'profile', f'{filename}')



class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
    )
    designation = models.CharField(max_length=100)

    profile_picture = models.ImageField(
        upload_to = user_profile_path, blank=True, null=True)

@receiver(post_delete, sender=UserProfile)
def delete_profile_picture(sender, instance, **kwargs):
    # Delete the profile picture file when a UserProfile instance is deleted
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)



class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(
        User, related_name='collaborators')

    created = models.DateTimeField()
    upated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ['-created']
    def __str__(self):
        return self.title


class Experiment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objective = models.CharField(max_length=200)
    notes = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Experiments'
        ordering = ['-created']
    def __str__(self):
        return "Expreiment ID:{} {}".format(self.id, self.objective[:20])

class Category(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '1.Categories'

    def __str__(self):
        return self.name


class Supplier(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '2.Suppliers'

    def __str__(self):
        return self.name


class Item(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    type_choice = [
        ('Solid', 'Solid'),
        ('Liquid', 'Liquid'),
        ('Gas', 'Gas'),
    ]
    type = models.CharField(max_length=20 ,choices=type_choice)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '3.Items'

    def __str__(self):
        return f'{self.name}'


class MeasurementUnit(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    short_name = models.CharField(max_length=10, unique=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '5.Measurmemt Units'

    def __str__(self):
        return self.name


class Inventory(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    batch = models.CharField(max_length=100)
    arrival_date = models.DateField()
    expiry_date = models.DateField()

    total_units = models.IntegerField()
    unit_size = models.FloatField()
    measurement_unit = models.ForeignKey(
        MeasurementUnit, on_delete=models.SET_NULL, null=True, blank=True)

    notes = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '6.Inventory'
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.item.name} ({self.batch} )'


class Formulation(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        Inventory, through='IngredientQuantity')
    name = models.CharField(max_length=200)
    atmosphere = models.CharField(max_length=10)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField()
    completed = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '8.Formulations'
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    formulation = models.ForeignKey(Formulation, on_delete=models.CASCADE)
    quantity = models.FloatField()
    measurement_unit = models.ForeignKey(
        MeasurementUnit, on_delete=models.SET_NULL, null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '7.Formulation Ingredients'
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.inventory.item.name}, {self.quantity} {self.measurement_unit.name} on {self.updated}'

class Layer(models.Model):

    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default='')

    name = models.CharField(max_length=100)
    coating_method_choices = (
        ('Spin Coating', 'Spin Coating'),
        ('Thermal Evaporation', 'Thermal Evaporation'),
    )
    coating_method = models.CharField(
        max_length=100, choices=coating_method_choices)

    layer_type = models.CharField(max_length=100)

    formulation = models.ForeignKey(Formulation, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.coating_method} - Layer {self.name}'
    
class SpinStep(models.Model):
    spin_speed = models.IntegerField()
    spin_acceleration = models.IntegerField()
    spin_time = models.IntegerField()

    class Meta:
        verbose_name_plural = '9.Spin Steps'

    def __str__(self):
        return f'Speed-{self.spin_speed} rpm, Acc-{self.spin_acceleration} rpm, {self.spin_time} s'


class SpinProgram(models.Model):
    name = models.CharField(max_length=100, default='')
    program = models.ManyToManyField(SpinStep)

    class Meta:
        verbose_name_plural = '10.Spin Program'

    def __str__(self):
        return self.name


class SpinCoatingCondition(models.Model):

    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default='')

    layer = models.OneToOneField(Layer, on_delete=models.CASCADE)

    program = models.ForeignKey(SpinProgram, on_delete=models.CASCADE)

    formulation_volume = models.FloatField()

    antisolvent_used = models.BooleanField(default=False)
    antisolvent = models.ForeignKey(
        Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    antisolvent_volume = models.FloatField(null=True, blank=True)
    antisolvent_drop_time = models.IntegerField(null=True, blank=True)

    room_temperature = models.IntegerField()
    room_humidity = models.IntegerField()

    atmosphere = models.CharField(max_length=50)

    drying_type = models.CharField(
        max_length=50, null=True, blank=True)
    drying_temperature = models.IntegerField(null=True, blank=True)
    drying_time = models.IntegerField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Spin Conditions'

    def __str__(self):
        return f'Spin Coated {self.layer.name}'



class ThermalEvaporationCondition(models.Model):
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE)
    layer = models.OneToOneField(Layer, on_delete=models.CASCADE)
    pressure = models.FloatField()



class Stack(models.Model):
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE)

    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    substrate = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    geometry_choices = (
        ('N-I-P', 'N-I-P'),
        ('P-I-N', 'P-I-N'),
        ('Power-Roll', 'Power-Roll'),
        ('Other', 'Other')
    )
    geometry = models.CharField(
        max_length=100, choices=geometry_choices)
    layers = models.ManyToManyField(Layer, through='StackLayerRelationShip')

    number_of_layers = models.IntegerField(default=0)
    number_of_devices = models.IntegerField(default=0)

    completed = models.BooleanField(default=False)

    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '11.Stacks'
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class StackLayerRelationShip(models.Model):
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    

    added_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '12.StackLayerRelationShip'
        ordering = ['-added_at']