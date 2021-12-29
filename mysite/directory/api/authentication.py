from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class TokenAuthentication(TokenAuthentication):
    """
    Simple token based authentication.
    """
    model = Token

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.')
            )

        return (token.user, token)
