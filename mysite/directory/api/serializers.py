from django.contrib.auth import get_user_model
from rest_framework import serializers
from directory.api.fields import SameCompanySlugRelatedField


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    reports_to = SameCompanySlugRelatedField(
        relation_field="company",
        slug_field="pk",
        queryset=User.objects.all(),
        allow_null=True,
        required=False
    )
    company = serializers.SlugRelatedField(
        slug_field='pk',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'pk',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'reports_to',
            'company',
        ]
        read_only_fields = [
            "pk"
        ]
