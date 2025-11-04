import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Role, Permission, ResourceType, Action
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserProfileSerializer, RoleSerializer, PermissionSerializer
)
from .permissions import HasPermission, IsAdminUser


def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_jwt_token(user)
            return Response({
                'token': token,
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_jwt_token(user)
            user.last_login = timezone.now()
            user.save()
            return Response({
                'token': token,
                'user': UserProfileSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        return Response({'message': 'Successfully logged out'})


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def update(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def delete_account(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'Account deleted successfully'})


class ProjectViewSet(viewsets.ViewSet):
    resource_type = 'project'
    permission_classes = [IsAuthenticated, HasPermission]

    def list(self, request):
        self.action_name = 'read'
        projects = [
            {'id': 1, 'name': 'Project Alpha', 'status': 'active'},
            {'id': 2, 'name': 'Project Beta', 'status': 'completed'},
        ]
        return Response(projects)

    def create(self, request):
        self.action_name = 'create'
        return Response({'message': 'Project created'}, status=status.HTTP_201_CREATED)


class DocumentViewSet(viewsets.ViewSet):
    resource_type = 'document'
    permission_classes = [IsAuthenticated, HasPermission]

    def list(self, request):
        self.action_name = 'read'
        documents = [
            {'id': 1, 'title': 'Technical Spec', 'type': 'specification'},
            {'id': 2, 'title': 'User Manual', 'type': 'manual'},
        ]
        return Response(documents)

    def create(self, request):
        self.action_name = 'create'
        return Response({'message': 'Document created'}, status=status.HTTP_201_CREATED)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
