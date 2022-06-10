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
    boosts = Boost.objects.filter(core=core)  # Достаем бусты пользователя из базы

    return render(request, 'index.html', {
            'core': core,
            'boosts': boosts,
            # Возвращаем бусты на фронтик
        })


@api_view(['GET'])
@login_required
def call_click(request):
    core = Core.objects.get(user=request.user)
    is_levelup = core.click()
    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level * 2)
    core.save()
    return Response({
        'core': CoreSerializer(core).data,
        'is_levelup': is_levelup,
    })


@api_view(
    [
        'POST'])
def update_coins(
        request):
    coins = request.data['current_coins']  # Значение current_coins будем присылать в теле запроса.
    core = Core.objects.get(user=request.user)

    is_levelup, boost_type = core.set_coins(coins)  # Метод set_coins скоро добавим в модель. Добавили boost_type для создания буста.

    # Дальнейшая логика осталась прежней, как в call_click
    if is_levelup:
        Boost.objects.create(
            core=core,
            price=core.coins,
            power=core.level * 2,
            type=boost_type)  # Создание буста. Добавили атрибут type.
    core.save()

    return Response(
        {
            'core': CoreSerializer(core).data,
            'is_levelup': is_levelup,
        })


@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({'core': CoreSerializer(core).data})


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts

    def partial_update(self, request, pk):
        coins = request.data['coins']  # Получаем количество монет из тела запроса.
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup(coins)  # Передадим количество монет в метод. Этот метод мы скоро немного подкорректируем.
        if not is_levelup:
            return Response({"error": "Не хватает денег"})
        old_boost_stats, new_boost_stats = is_levelup

        return Response({
                "old_boost_stats": self.serializer_class(old_boost_stats).data,
                "new_boost_stats": self.serializer_class(new_boost_stats).data,
            })


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

        return render(request, 'register.html', {'user_form': user_form, 'invalid': True})


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