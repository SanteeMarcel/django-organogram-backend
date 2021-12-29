from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from directory.api.filtersets import UsersFilterSet
from directory.api.serializers import UserSerializer
from directory.models import User
from typing import List, Set

class UsersViewSet(viewsets.ModelViewSet):
    """
    Endpoint for returning User data.
    """
    filterset_class = UsersFilterSet
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def reports(self, request, pk):
        user = self.get_object()
        users = reportees(user)
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer: UserSerializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['get'])
    def managers(self, request, pk):
        user = self.get_object()
        users = managers(user)
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer: UserSerializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=200)

    def get_queryset(self):
        users = User.objects.filter(company=self.request.user.company)
        return users

# Recursive function
# VERY inefficient, it would be better have a pointer pointing down
def reportees(user: User) -> Set[User]:

    users = User.objects.filter(company=user.company)

    total_reportees = set()

    for employee in users:
        if _reportees(employee, user):
            total_reportees.add(employee)
    
    return total_reportees

def _reportees(user: User, desired_reportee: User) -> bool:
    # base cases
    if user.reports_to == desired_reportee:
        return True
    elif user.reports_to is None:
        return False
    # recursion
    return _reportees(user.reports_to, desired_reportee)

def managers(user: User) -> List[User]:

    employee = user

    managers = set()

    while employee.reports_to:
        managers.add(employee.reports_to)

        employee = employee.reports_to

    return managers