from django.core.management.base import BaseCommand
from auth_system.backend.auth_app.models import ResourceType, Action, Permission, Role, User


class Command(BaseCommand):
    help = 'Seed initial data for the auth system'

    def handle(self, *args, **options):
        resource_types = [
            ('project', 'Проекты'),
            ('document', 'Документы'),
            ('user', 'Пользователи'),
        ]

        for name, description in resource_types:
            ResourceType.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )

        actions = [
            ('create', 'Создание'),
            ('read', 'Чтение'),
            ('update', 'Обновление'),
            ('delete', 'Удаление'),
            ('manage', 'Управление'),
        ]

        for name, description in actions:
            Action.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )

        permissions_data = [
            ('project', 'create', 'Создание проектов'),
            ('project', 'read', 'Просмотр проектов'),
            ('project', 'update', 'Обновление проектов'),
            ('project', 'delete', 'Удаление проектов'),
            ('document', 'create', 'Создание документов'),
            ('document', 'read', 'Просмотр документов'),
            ('document', 'update', 'Обновление документов'),
            ('document', 'delete', 'Удаление документов'),
        ]

        for resource_type, action, name in permissions_data:
            rt = ResourceType.objects.get(name=resource_type)
            act = Action.objects.get(name=action)
            Permission.objects.get_or_create(
                resource_type=rt,
                action=act,
                defaults={'name': name}
            )

        roles_data = [
            ('admin', 'Администратор системы'),
            ('manager', 'Менеджер проектов'),
            ('user', 'Обычный пользователь'),
        ]

        admin_role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Администратор системы'}
        )

        all_permissions = Permission.objects.all()
        admin_role.permissions.set(all_permissions)

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded initial data')
        )
