from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from djoser.serializers import SetPasswordSerializer

from .permissions import IsAuthorOrAdminOrReadOnly
from .paginations import Pagination
from .filters import RecipeFilter
from recipes.models import (Follow, Tag, Ingredient, Recipe, ShoppingCart,
                            Favorite, IngredientsInRecipe)
from .serializers import (FollowSerializer, UserSerializer, TagSerializer,
                          IngredientSerializer, RecipeViewSerializer,
                          RecipeWriteSerializer, FavoriteSerializer,
                          ShoppingCartSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = Pagination
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=["post"],
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data,
                                           context={'request': request})
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response('Изменение пароля прошло успешно',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=self.request.data.get('id'))
        user = self.request.user
        if request.method == 'POST':
            serializer = FollowSerializer(
                data=request.data,
                context={'request': request, 'author': author})
            if not serializer.is_valid(raise_exception=True):
                return Response({'errors': 'Пользователь не найден'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer.save(author=author, user=user)
            return Response({'Успешная подписка на пользователя':
                            serializer.data},
                            status=status.HTTP_201_CREATED)

        if not Follow.objects.filter(author=author, user=user).exists():
            return Response({'errors':
                            f'Вы не подписаны на пользователя {author}'},
                            status=status.HTTP_404_NOT_FOUND)
        Follow.objects.get(author=author).delete()
        return Response('Успешная отписка', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        follows = Follow.objects.filter(user=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = Pagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeViewSerializer
        return RecipeWriteSerializer

    def add_or_delete_recipe(self, request, model, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        data = {'user': user.id, 'recipe': recipe.id}
        if request.method == 'POST':
            if model.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен!'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if not model.objects.filter(user=user,
                                    recipe=recipe).exists():
            return Response({'errors': 'Объект не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        model.objects.get(recipe=recipe).delete()
        return Response('Рецепт успешно удалён.',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        self.add_or_delete_recipe(request, Favorite, FavoriteSerializer)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, **kwargs):
        return self.add_or_delete_recipe(request, ShoppingCart,
                                         ShoppingCartSerializer)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, **kwargs):
        user = User.objects.get(id=self.request.user.pk)
        sum_ingredients = IngredientsInRecipe.objects.filter(
            recipe__shopping_cart__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amounts=Sum('amount'))

        shopping_list = '\n'.join(
            [f'{ingredient["ingredient__name"]} {ingredient["amounts"]} '
             f'{ingredient["ingredient__measurement_unit"]}'
             for ingredient in sum_ingredients])
        response = HttpResponse(shopping_list, content_type='text/plain')
        return response
