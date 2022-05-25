from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import CoreSerializer, BoostSerializer
from .models import Core, Boost
from .forms import UserForm


@login_required # For reg users view index.html
def index(request):
    core = Core.objects.get(user=request.user)
    boosts = Boost.objects.filter(
        core=core)  # Достаем бусты пользователя из базы

    return render(
        request,
        'index.html',
        {
            'core': core,
            'boosts': boosts,
            # Возвращаем бусты на фронтик
        })


@api_view(['GET'])
def call_click(request):
    core = Core.objects.get(user=request.user)
    is_levelup = core.click()
    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level*20)
    return Response({
        'core': CoreSerializer(core).data,
        'is_levelup': is_levelup,
    })


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts


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