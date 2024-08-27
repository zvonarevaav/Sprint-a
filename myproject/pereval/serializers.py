from drf_writable_nested import WritableNestedModelSerializer
from .models import *
from rest_framework import serializers


class MoUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoUser
        fields = [
            'email',
            'phone',
            'fam',
            'name',
            'otc',
        ]
        verbose_name = 'Турист'

    def save(self, **kwargs):
        self.is_valid()
        user = MoUser.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = MoUser.objects.create(
                email=self.validated_data.get('email'),
                phone=self.validated_data.get('phone'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
            )
            return new_user


class CoordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coords
        fields = [
            'latitude',
            'longitude',
            'height'
        ]
        verbose_name = 'Координаты'


class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = [
            'winter',
            'summer',
            'autumn',
            'spring'
        ]
        verbose_name = 'Уровень сложности'


class ImagesSerializer(serializers.ModelSerializer):
    image = serializers.URLField()

    class Meta:
        model = Images
        fields = [
            'image',
            'title',
        ]
        verbose_name = 'Фото'


class MountpassSerializer(WritableNestedModelSerializer, serializers.HyperlinkedModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user = MoUserSerializer()
    coord = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)
    id = serializers.HyperlinkedIdentityField(view_name='mountpass-detail')  # Вывод данных по ид

    class Meta:
        model = Mountpass
        fields = [
            'id',
            'beautyTitle',
            'title',
            'other_titles',
            'connect',
            'add_time',
            'user',
            'coord',
            'level',
            'images',
            'status',
        ]
        read_only_fields = ['status']

    # Запрет изменять данные пользователя при редактировании данных о перевале
    def validate(self, data):

        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError(
                    {
                        'ФИО, email и номер телефона пользователя не могут быть изменены'
                    }
                )
        return data