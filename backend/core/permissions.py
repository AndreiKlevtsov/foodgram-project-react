from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Полные права на управление всем контентом проекта только у администратора.
    Незарегистрированным пользователям доступно чтение.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Права на изменение у администратора и автора.
    Незарегистрированным пользователям доступно чтение.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
