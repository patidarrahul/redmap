from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Project)
admin.site.register(Experiment)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Item)
admin.site.register(MeasurementUnit)
admin.site.register(Inventory)
admin.site.register(Formulation)
admin.site.register(IngredientQuantity)
admin.site.register(Layer)
admin.site.register(SpinCoatingCondition)
admin.site.register(SpinProgram)
admin.site.register(SpinStep)
admin.site.register(ThermalEvaporationCondition)
admin.site.register(Stack)
admin.site.register(StackLayerRelationShip)
admin.site.register(UserProfile)
