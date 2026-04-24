from typing import Optional, Tuple

from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import UntypedToken

from apps.accounts.models import PlatformUser
from apps.platforms.models import Platform


class PlatformJWTAuthentication(authentication.BaseAuthentication):
    www_authenticate_realm = "api"

    def authenticate(self, request) -> Optional[Tuple[PlatformUser, str]]:
        header = authentication.get_authorization_header(request).decode("utf-8")
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        raw_token = parts[1]

        try:
            UntypedToken(raw_token)
        except TokenError as exc:
            raise AuthenticationFailed(_("Invalid token.")) from exc

        token_backend = TokenBackend(
            algorithm=api_settings.ALGORITHM,
            signing_key=api_settings.SIGNING_KEY,
            verifying_key=api_settings.VERIFYING_KEY,
            audience=api_settings.AUDIENCE,
            issuer=api_settings.ISSUER,
            jwk_url=api_settings.JWK_URL,
            leeway=api_settings.LEEWAY,
        )

        try:
            payload = token_backend.decode(raw_token, verify=True)
        except TokenError as exc:
            raise AuthenticationFailed(_("Invalid token.")) from exc

        platform_user_id = payload.get("platform_user_id")
        platform_id = payload.get("platform_id")
        if not platform_user_id or not platform_id:
            raise AuthenticationFailed(_("Token missing platform context."))

        try:
            user = PlatformUser.objects.select_related("platform").get(
                id=platform_user_id
            )
        except PlatformUser.DoesNotExist as exc:
            raise AuthenticationFailed(_("User not found.")) from exc

        if user.platform_id != platform_id:
            raise AuthenticationFailed(_("Token platform mismatch."))

        try:
            platform = Platform.objects.get(id=platform_id)
        except Platform.DoesNotExist as exc:
            raise AuthenticationFailed(_("Platform not found.")) from exc

        request.platform = platform
        request.platform_user = user

        return (user, raw_token)

    def authenticate_header(self, request) -> str:
        return f'Bearer realm="{self.www_authenticate_realm}"'
