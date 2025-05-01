from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .models import User

class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        data = request.POST
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        role = data.get('role')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        id_number = data.get('id_number', '').strip()
        level = data.get('level') if role == 'student' else None
        term = data.get('term') if role == 'student' else None
        contact_information = data.get('contact_information', '').strip()

        # Validation
        if not all([name, email, role, password, id_number, contact_information]):
            messages.error(request, "All fields are required.")
            return redirect('accounts:register')

        if role == 'student' and not all([level, term]):
            messages.error(request, "Level and Term are required for students.")
            return redirect('accounts:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('accounts:register')

        if User.objects.filter(id_number=id_number).exists():
            messages.error(request, "ID number already exists.")
            return redirect('accounts:register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('accounts:register')
        
        try:
            User.objects.create_user(
                email=email,
                name=name,
                role=role,
                id_number=id_number,
                level=level,
                term=term,
                contact_information=contact_information,
                password=password
            )
            messages.success(request, "Registration successful! Please login.")
            return redirect('accounts:login')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return redirect('accounts:register')

class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('profiles:profile')
        messages.error(request, "Invalid credentials.")
        return redirect('accounts:login')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home:index')