from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from buho_backend.utils.token_utils import ExpiringTokenAuthentication

from settings.models import UserSettings
from settings.serializers import UserSettingsSerializer


class UserSettingsListAPIView(APIView):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    # test
    # 1. List all
    @swagger_auto_schema(tags=["settings"])
    def get(self, request, *args, **kwargs):
        """
        List all the market items for given requested user
        """
        todo = UserSettings.objects.get(user=request.user.id)
        serializer = UserSettingsSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSettingsDetailAPIView(APIView):
    # add permission to check if user is authenticated
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, todo_id, user_id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return UserSettings.objects.get(id=todo_id, user=user_id)
        except UserSettings.DoesNotExist:
            return None

    # 3. Retrieve
    @swagger_auto_schema(tags=["settings"])
    def get(self, request, market_id, *args, **kwargs):
        """
        Retrieves the Todo with given todo_id
        """
        todo_instance = self.get_object(market_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserSettingsSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    @swagger_auto_schema(tags=["settings"], request_body=UserSettingsSerializer)
    def put(self, request, settings_id, *args, **kwargs):
        """
        Updates the settings item with given todo_id if exists
        """
        todo_instance = self.get_object(settings_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with settings id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "companyDisplayMode": request.data.get("companyDisplayMode"),
            "companySortBy": request.data.get("companySortBy"),
            "language": request.data.get("language"),
            "timezone": request.data.get("timezone"),
            "mainPortfolio": request.data.get("mainPortfolio"),
            "portfolioSortBy": request.data.get("portfolioSortBy"),
            "portfolioDisplayMode": request.data.get("portfolioDisplayMode"),
        }
        serializer = UserSettingsSerializer(
            instance=todo_instance, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
