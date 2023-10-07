import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def user_profile_path(self, filename):
        """
        Generate the user profile path for a given filename.

        Args:
            filename (str): The name of the file.

        Returns:
            str: The path of the user's profile file.
        """
        username = self.user.username
        ext = filename.split('.')[-1]
    

        return os.path.join('users', username, 'profile', f'{filename}')


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
    )
    designation = models.CharField(max_length=100)

    profile_picture = models.ImageField(
        upload_to = user_profile_path, blank=True, null=True)
    


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
