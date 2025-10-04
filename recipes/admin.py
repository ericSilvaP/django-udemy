from django.contrib import admin
from .models import Recipe, Category


class CategoryAdmin(admin.ModelAdmin): ...


class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "is_published"]
    list_display_links = ["title", "author"]
    list_editable = ["is_published"]
    list_filter = ["author", "is_published"]
    ordering = ["-id"]
    list_per_page = 10


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
