from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers import PlatformUserLoginSerializer, PlatformUserRegisterSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PlatformUserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                'id': user.id,
                'platform_id': user.platform_id,
                'platform_slug': user.platform.slug,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PlatformUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'refresh': serializer.validated_data['refresh'],
                'access': serializer.validated_data['access'],
            },
            status=status.HTTP_200_OK,
        )
