from django.contrib.auth import login
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .custom_response import CustomResponse, CustomErrors
from .models import *


class SignUpUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'password', 'date_of_birth']

    def save(self, **kwargs):
        if self.is_valid():
            user = CustomUser(
                username=self.validated_data['username'],
                nickname=self.validated_data['nickname'],
                date_of_birth=self.validated_data['date_of_birth']
            )
            user.token = CustomUser.generate_token(user.username)
            user.set_password(
                self.validated_data['password']
            )
            user.save()

            login(kwargs['request'], user)

            return CustomResponse({
                'message': ['Регистрация успешно завершена.'],
                'token': user.token
            }).good()
        else:
            return CustomResponse(self.errors).bad()


class EditUserSerializer(Serializer):
    token = serializers.CharField()
    username = serializers.CharField(required=True, max_length=20)
    nickname = serializers.CharField(required=True, max_length=9)
    status_emoji = serializers.CharField(max_length=1)
    status = serializers.CharField(max_length=20)


class SignUserSerializer(Serializer):
    username = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(required=True)

    def save(self, **kwargs):
        if self.is_valid():
            queryset = CustomUser.objects.filter(
                username=kwargs['username']
            )
            if queryset:
                user = queryset[0]
                if user.check_password(
                        kwargs['password']
                ):
                    return CustomResponse({
                        'message': 'Токен успешно получен.',
                        'token': user.token
                    }).good()
                return CustomResponse(
                    CustomErrors('password').object_not_found_error()
                ).bad()
            return CustomResponse(
                CustomErrors('username').object_not_found_error()
            ).bad()
        else:
            return CustomResponse(self.errors).bad()


class SubscribeToUserSerialuzer(Serializer):
    token = serializers.CharField(required=True)
    username = serializers.CharField(required=True, max_length=20)

    def save(self, **kwargs):
        if not kwargs['user1'] in kwargs['user'].subscribers.all():
            kwargs['user'].subscribers.add(kwargs['user1'])
            kwargs['user1'].subscriptions.add(kwargs['user'])
            return CustomResponse({
                'message': [f'Подписка на '
                           f'{self.validated_data["username"]} '
                           f'оформлена.'],
                'subscrube_status': 1
            }).good()


        else:
            kwargs['user'].subscribers.remove(kwargs['user1'])
            kwargs['user1'].subscriptions.remove(kwargs['user'])
            return CustomResponse({
                'message': [f'Подписка на '
                           f'{self.validated_data["username"]} '
                           f'отменена.'],
                'subscrube_status': 0
            }).good()

    def validated_title(self, value):
        if not value:
            return False
        if not value[0].pk:
            return False
        return value[0]


class UserAPITokenSerializer(Serializer):
    token = serializers.CharField()

    def save(self, **kwargs):
        if self.is_valid():
            queryset = CustomUser.objects.filter(
                token=self.validated_data['token']
            )
            if queryset:
                user = queryset[0]
                user.token = CustomUser.generate_token(user.username)
                user.save()
                return CustomResponse({
                    'message': ['Авторизация успешно завершена.'],
                    'token': user.token
                }).good()
            return CustomResponse(
                CustomErrors('token').object_not_found_error()
            ).bad()
        else:
            return CustomResponse(self.errors).bad()


class CreatePostSerializer(Serializer):
    token = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    theme = serializers.CharField(required=False)


class CreateCommentSerializer(Serializer):
    post_id = serializers.IntegerField(required=True)
    token = serializers.CharField(required=True)
    text = serializers.CharField(required=True)


class LikeModelSerializer(Serializer):
    id = serializers.IntegerField(required=True)
    model_name = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def save(self, **kwargs):
        if self.is_valid():
            user = CustomUser.objects.filter(
                token=self.validated_data['token']
            )
            if user:
                user = user[0]

                if self.validated_data['model_name'] == 'post':
                    model = Post
                elif self.validated_data['model_name'] == 'comment':
                    model = Comment

                model = model.objects.filter(
                    pk=self.validated_data['id']
                )
                if model:
                    model = model[0]
                    if user in model.likes.all():
                        model.likes.remove(
                            user
                        )
                        return CustomResponse({
                            'message': ['Объект удалён.'],
                            'like_status': 0
                        }).good()
                    else:
                        model.likes.add(
                            user
                        )
                        return CustomResponse({
                            'message': ['Объект создан.'],
                            'like_status': 1
                        }).good()
                else:
                    return CustomResponse(
                        CustomErrors('model_name').object_not_found_error()
                    ).bad()
            else:
                return CustomResponse(
                    CustomErrors('token').object_not_found_error()
                ).bad()
        else:
            return CustomResponse(self.errors).bad()


class GetPostSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)

    class Meta:
        model = Post
        fields = ('pk', 'owner', 'date_of_creation', 'text',)


class DeletePostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=True)
    token = serializers.CharField(required=True)


class DeleteCommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField(required=True)
    token = serializers.CharField(required=True)
