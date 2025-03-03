from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает редактирование и удаление только владельцу задачи.
    Остальным пользователям — только чтение.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True  # GET, HEAD, OPTIONS разрешены всем
        return obj.user == request.user  # Разрешаем изменение только владельцу
