# Схема базы данных системы аутентификации и авторизации

## Таблицы

### users
- id (PK)
- email (UNIQUE)
- first_name
- last_name 
- middle_name
- password
- is_active
- is_staff
- is_superuser
- date_joined
- last_login

### resource_types
- id (PK)
- name (UNIQUE)
- description

### actions  
- id (PK)
- name (UNIQUE)
- description

### permissions
- id (PK)
- resource_type_id (FK → resource_types)
- action_id (FK → actions)
- name
- description
- UNIQUE(resource_type_id, action_id)

### roles
- id (PK)
- name (UNIQUE)
- description

### role_permissions (M2M)
- id (PK)
- role_id (FK → roles)
- permission_id (FK → permissions)

### user_roles (M2M)
- id (PK)
- user_id (FK → users)
- role_id (FK → roles)
- assigned_at
- UNIQUE(user_id, role_id)

### user_permissions (M2M)
- id (PK)
- user_id (FK → users)
- permission_id (FK → permissions)
- granted_at
- UNIQUE(user_id, permission_id)

## Логика доступа

Права доступа определяются по принципу:
- Пользователь имеет разрешение если:
  1. Ему напрямую назначено это разрешение ИЛИ
  2. Ему назначена роль, которая содержит это разрешение
- Суперпользователь имеет все права всегда