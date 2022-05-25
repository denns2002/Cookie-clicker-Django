from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import login, logout, authenticate
from .models import Core
from rest_framework.decorators import api_view
from rest_framework.response import Response


@login_required # For reg users view index.html
def index(request):
    core = Core.objects.get(user=request.user)
    return render(request, 'index.html', {'core': core})

@api_view(['GET'])
def call_click(request):
    core = Core.objects.get(user=request.user)
    core.click()
    return Response({'coins': core.coins})

class Register(APIView):
    def get(self, request):
        user_form = UserForm()
        return render(request, 'register.html', {'user_form': user_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)

            core = Core(user=user)
            core.save()
            return redirect('index')

        return render(request, 'register.html', {'user_form': user_form})


class Login(APIView):
    user_form = UserForm()

    def get(self, request):
        return render(request, 'login.html', {'user_form': self.user_form})

    def post(self, request):
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('index')

        return render(request, 'login.html', {
            'user_form': self.user_form, 'invalid': True
        })

def user_logout(request):
    logout(request)
    return redirect('login')