from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Core, Boost


class CoreSerializer(ModelSerializer):
    class Meta:
        model = Core
        fields = ['coins', 'click_power', 'auto_click_power', 'next_level_price'] # Добавляем поле next_level_price, которое нужно вернуть на фронт.

    next_level_price = SerializerMethodField() # Поле, которое соответствует вычисляемому значению.

    # Метод вычисления значения для поля next_level_price.
    def get_next_level_price(self, obj):
        return obj.calculate_next_level_price() # obj - экземпляр модели Core.


class BoostSerializer(ModelSerializer):
    class Meta:
        model = Boost
        fields = '__all__'