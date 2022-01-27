# from rest_framework import permissions

from django.contrib.auth.models import Permission

#
# class IsMentorCoursePermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if view.action in ['create', 'delete']:
#             return request.user.is_superuser
#         if view.action == 'update':
#             obj = view.queryset.first()
#             return request.user.is_authenticated and (
#                     request.user.is_superuser
#             )
#         return True