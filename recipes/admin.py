from django.contrib import admin
from .models import Recipe, Category


# Register your models here.
class RecipeAdmin(admin.ModelAdmin): ...


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)
