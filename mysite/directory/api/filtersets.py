from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from rest_framework import filters

User = get_user_model()

class UsersFilterSet(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet, view):
        return queryset.defer("email", "is_active")

class HasManagerFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet, view):
        has_manager = request.query_params.get("has_manager", None)
        if has_manager in ("true", "false"):
            if has_manager  == "true":
                return queryset.filter(reports_to_id__isnull=False)
            else:
                return queryset.filter(reports_to_id__isnull=True)
            
        return queryset

class IsManagerFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet, view):
        is_manager = request.query_params.get("is_manager", None)
        if is_manager in ("true", "false"):

            users = queryset.all()
            managers_ids = set()
            for user in users:
                if user.reports_to:
                    managers_ids.add(user.reports_to.id)

            if is_manager  == "true":
                return queryset.filter(pk__in=managers_ids)
            else:
                return queryset.exclude(pk__in=managers_ids)
        return queryset