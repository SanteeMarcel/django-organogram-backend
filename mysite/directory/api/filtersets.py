from django.db.models.query import QuerySet
from django_filters import rest_framework as filters, BooleanFilter
from django.contrib.auth import get_user_model


User = get_user_model()


class UsersFilterSet(filters.FilterSet):
    strict = True
    has_manager = BooleanFilter(field_name="reports_to", method="verify_reports_up")
    is_manager = BooleanFilter(field_name="reports_to", method="find_reportees")

    class Meta:
        model = User
        fields = [
            'reports_to'
        ]

    def find_reportees(self, queryset: QuerySet, name, value):
        if value:
            queryset = queryset.filter()
            return queryset
        queryset = queryset.filter()
        return queryset

    def verify_reports_up(self, queryset: QuerySet, name, value):
        if value:
            queryset = queryset.filter(reports_to_id__isnull=False)
            return queryset
        queryset = queryset.filter(reports_to_id__isnull=True)
        return queryset