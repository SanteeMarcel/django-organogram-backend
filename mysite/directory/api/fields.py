from rest_framework import serializers
from directory.models import Company


class JsonSerializerableMultipleChoiceField(serializers.MultipleChoiceField):
    def to_representation(self, value):
        return list(super().to_representation(value))


class SameCompanySlugRelatedField(serializers.SlugRelatedField):
    """For many of our related fields (departments, locations, reports_to, etc)
    it is vitally important that the assigned field is within the same
    organization.

    DRF provides very little to enforce this besides using validators after
    submission (which is already included in a few serializers). However, the
    HTML forms in the API View are able to see the possible querysets, which by
    default were Model.objects.all() for most SlugRelatedFields. This causes a
    data leak were a user could see emails, departments, etc across Companies.

    To remedy, we need to reduce the filterset with DRF's API View (or anyone
    else) asks for it.

    This Class is used to filter down a queryset to only be within the
    caller's org. It can be dynamically queried during the instantiation of
    the class.

    Passing in the relation_field, as the dundered relation for the query. This
    class will filter to make sure that passed relation_field is the company
    on the calling user.

    Pass the "*" attribute to self-reference company, for when the related
    field is the company object.
    """
    def __init__(self, relation_field, *args, **kwargs):
        self.relation_field = relation_field
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        user = self.context['request'].user
        company_value = user.profile.company
        assert isinstance(company_value, Company)
        if self.relation_field == "*":
            relation_field = "uuid"
            company_value = company_value.uuid
        else:
            relation_field = self.relation_field
            company_value = user.profile.company
        queryset = self.queryset.filter(**{relation_field: company_value})
        return queryset
