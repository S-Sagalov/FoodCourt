from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, TagViewSet, IngredientViewSet, RecipeViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
