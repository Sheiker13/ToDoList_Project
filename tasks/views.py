from rest_framework import viewsets, permissions
from .models import Task, Tag, Comment, Category
from .serializers import TaskSerializer, TagSerializer, CommentSerializer, CategorySerializer
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import action
from .tasks import send_task_notification
from .permissions import IsOwnerOrReadOnly
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

# Фильтр для категорий
class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Поиск по имени

    class Meta:
        model = Category
        fields = ['name']

# ViewSet для задач
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # Закрываем доступ для неавторизованных пользователей

    def perform_create(self, serializer):
        task = serializer.save(author=self.request.user)
        cache.delete("tasks_list")  # Очищаем кеш при изменениях
        send_task_notification.delay(task.author.email, task.title)  # Асинхронный вызов

    @action(detail=False, methods=['get'])
    def cached_list(self, request):
        tasks = cache.get("tasks_list")
        if not tasks:
            tasks = list(self.get_queryset())  # Преобразуем QuerySet в список
            cache.set("tasks_list", tasks, timeout=60)  # Кешируем на 1 минуту
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

# ViewSet для тегов
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]  # Разрешаем всем

# ViewSet для комментариев
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# ViewSet для категорий
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  # Разрешаем всем
    filter_backends = (DjangoFilterBackend,)  # Добавляем фильтрацию
    filterset_class = CategoryFilter  # Подключаем фильтр

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def cached_list(self, request):
        categories = cache.get("category_list")
        if not categories:
            categories = self.get_queryset()
            cache.set("category_list", categories, timeout=600)  # Кешируем на 10 минут
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
