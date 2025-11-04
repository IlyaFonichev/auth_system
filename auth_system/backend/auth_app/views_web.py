from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import User
from .serializers import UserRegistrationSerializer


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return self._redirect_user(request.user)
        return render(request, 'auth_app/registration.html')

    def post(self, request):
        if request.user.is_authenticated:
            return self._redirect_user(request.user)

        serializer = UserRegistrationSerializer(data=request.POST)

        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти в систему.')
            return redirect('login_view')
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'auth_app/registration.html', {'form': request.POST})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return self._redirect_user(request.user)
        return render(request, 'auth_app/login.html')

    def post(self, request):
        if request.user.is_authenticated:
            return self._redirect_user(request.user)

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден или аккаунт деактивирован.')
            return render(request, 'auth_app/login.html')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return self._redirect_user(user)
        else:
            messages.error(request, 'Неверный пароль.')
            return render(request, 'auth_app/login.html')

    def _redirect_user(self, user):
        if user.is_staff or user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('profile_view')


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login_view')
        return render(request, 'auth_app/profile.html', {'user': request.user})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login_view')

        action = request.POST.get('action')
        user = request.user

        if action == 'update':
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.middle_name = request.POST.get('middle_name', user.middle_name)

            user.save()
            messages.success(request, 'Информация успешно обновлена!')

        elif action == 'delete':
            user.is_active = False
            user.save()

            logout(request)
            messages.success(request, 'Ваш аккаунт был успешно удален.')
            return redirect('login_view')

        return redirect('profile_view')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
        return redirect('login_view')
