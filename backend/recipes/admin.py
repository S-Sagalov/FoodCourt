from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, Recipe, ShoppingCart, Tag,
                     IngredientsInRecipe)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientsInline(admin.TabularInline):
    model = IngredientsInRecipe
    min_num = 1
    extra = 2


class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    list_filter = ('recipe', 'ingredient')
    search_fields = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'pub_date', 'in_favorite',)
    search_fields = ('name',)
    list_filter = ('pub_date', 'author', 'name', 'tags')
    filter_horizontal = ('ingredients',)
    inlines = [IngredientsInline]
    empty_value_display = '-'

    def in_favorite(self, obj):
        return obj.favorite.all().count()


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'hex_code')


admin.site.register(IngredientsInRecipe, IngredientsInRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
