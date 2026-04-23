from drf_spectacular.extensions import OpenApiAuthenticationExtension

from apps.accounts.authentication import PlatformJWTAuthentication


class PlatformJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = PlatformJWTAuthentication
    name = 'bearerAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
