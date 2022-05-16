from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response
from .custom_response import CustomResponse, CustomErrors
from django.db import models
from .serializers import *
from .models import *


class CheckField:
    def __init__(self, field):
        self.field = field

    def check(self):
        if self.field:
            return self.field[0]


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = SignUpUserSerializer(
            data=request.data
        )

        return serializer.save(
            request=request
        )


class UpdateAuthTokenAPIView(APIView):
    def post(self, request):
        serializer = UserAPITokenSerializer(
            data=request.data
        )

        return serializer.save(
            request=request
        )


class GetAuthTokenAPIView(APIView):
    def post(self, request):
        serializer = SignUserSerializer(
            data=request.data
        )
        return serializer.save(
            request=request
        )


class SignInAPIView(APIView):
    def post(self, request):
        serializer = SignUserSerializer(
            data=request.data
        )
        if serializer.is_valid():
            queryset = CustomUser.objects.filter(
                username=request.data['username']
            )
            if queryset:
                user = queryset[0]
                if user.check_password(
                        request.data['password']
                ):
                    login(request, user)
                    return CustomResponse({
                        'message': ['Авторизация успешно завершена.'],
                        'token': user.token
                    }).good()
                return CustomResponse({
                    'password': ['Некорректный пароль.']
                }).bad()

            return CustomResponse(
                CustomErrors('username').object_not_found_error()
            ).bad()
        else:
            return CustomResponse(serializer.errors).bad()


class SignOutAPIView(APIView):
    def post(self, request):
        logout(request)

        return CustomResponse({
            'message': 'Вы вышли из аккаунта.'
        }).good()


class SubscribeToUserAPIView(APIView):
    def post(self, request):
        serializer = SubscribeToUserSerialuzer(
            data=request.data
        )

        if serializer.is_valid():
            user = serializer.validated_title(CustomUser.objects.filter(
                username=serializer.validated_data['username']
            ))
            if user:
                user1 = serializer.validated_title(CustomUser.objects.filter(
                    token=serializer.validated_data['token']
                ))
                if user1:
                    return serializer.save(user=user, user1=user1, validated_data=serializer.validated_data)
                CustomResponse(
                    CustomErrors('token').object_not_found_error()
                ).bad()
            return CustomResponse(
                    CustomErrors('username').object_not_found_error()
                ).bad()
        else:
            return CustomResponse(serializer.errors).bad()


class EditUserProfileAPIView(APIView):
    def post(self, request):
        serializer = EditUserSerializer(
            data=request.data
        )

        if serializer.is_valid():
            user = CustomUser.objects.filter(
                token=serializer.validated_data['token']
            )
            if user:
                user = user[0]
                if not CustomUser.objects.filter(
                        username=serializer.validated_data['username']
                ) or CustomUser.objects.filter(
                    username=serializer.validated_data['username']
                )[0] == user:
                    user.username = serializer.validated_data['username']
                    user.nickname = serializer.validated_data['nickname']

                    if 'avatar' in request.FILES:
                        user.avatar = request.FILES['avatar']

                    if 'status_emoji' in serializer.validated_data:
                        user.status_emoji = serializer.validated_data['status_emoji']
                    if 'status' in serializer.validated_data:
                        user.status = serializer.validated_data['status']
                    user.save()

                    return CustomResponse({
                        'message': 'Объект отредактирован.'
                    }).good()
                return CustomResponse(
                    CustomErrors('nickname').object_already_exists_error()
                ).bad()
            return CustomResponse(
                    CustomErrors('token').object_not_found_error()
                ).bad()
        else:
            return CustomResponse(serializer.errors).bad()


class CreatePostAPIView(APIView):
    def post(self, request):
        serializer = CreatePostSerializer(
            data=request.data
        )

        if serializer.is_valid():
            user = CustomUser.objects.filter(
                token=serializer.validated_data['token']
            )
            if user:
                user = user[0]
                post = Post()
                post.owner = user
                post.text = serializer.validated_data['text']
                post.theme = request.data['theme']
                if 'image' in request.FILES:
                    post.image = request.FILES['image']
                if 'music' in request.FILES:
                    post.music = request.FILES['music']
                if 'document' in request.FILES:
                    post.document = request.FILES['document']
                post.save()

                return CustomResponse({
                    'message': ['Объект создан.'],
                    'post_id': post.pk
                }).good()
            else:
                return CustomResponse(
                    CustomErrors('token').object_not_found_error()
                ).bad()
        else:
            return CustomResponse(serializer.errors).bad()


class DeletePostAPIView(APIView):
    def post(self, request):
        serializer = DeletePostSerializer(
            data=request.data
        )

        if serializer.is_valid():
            post = CheckField(Post.objects.filter(
                pk=serializer.validated_data['post_id']
            )).check()
            if post:
                user = CheckField(CustomUser.objects.filter(
                    token=serializer.validated_data['token']
                )).check()
                if user:
                    if post.owner == user:
                        post.delete()
                        return CustomResponse({
                            'message': ['Объект удалён.']
                        }).good()
                    else:
                        return CustomResponse(
                            CustomErrors('token').no_permission_error()
                        ).bad()
                else:
                    CustomResponse(
                        CustomErrors('comment_id').object_not_found_error()
                    ).bad()

            else:
                return CustomResponse(
                    CustomErrors('post_id').object_not_found_error()
                ).bad()
        else:
            return CustomResponse(serializer.errors).bad()


class DeleteCommentAPIView(APIView):
    def post(self, request):
        serializer = DeleteCommentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            comment = CheckField(Comment.objects.filter(
                pk=serializer.validated_data['comment_id']
            )).check()
            if comment:
                user = CheckField(CustomUser.objects.filter(
                    token=serializer.validated_data['token']
                )).check()
                if user:
                    if comment.owner == user:
                        comment.delete()

                        return CustomResponse({
                            'message': ['Объект удалён.']
                        }).good()
                    else:
                        return CustomResponse(
                            CustomErrors('token').no_permission_error()
                        ).bad()
                else:
                    CustomResponse(
                        CustomErrors('comment_id').object_not_found_error()
                    ).bad()
            else:
                return CustomResponse(
                    CustomErrors('comment_id').object_not_found_error()
                ).bad()
        else:
            return CustomResponse(serializer.errors).bad()


class LikeModelAPIView(APIView):
    def post(self, request):
        serializer = LikeModelSerializer(
            data=request.data
        )
        return serializer.save()


class CreateCommentAPIView(APIView):
    def post(self, request):
        serializer = CreateCommentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            user = CheckField(CustomUser.objects.filter(
                token=serializer.validated_data['token']
            )).check()
            if user:
                post = CheckField(Post.objects.filter(
                    pk=serializer.validated_data['post_id']
                )).check()
                if post:
                    comment = Comment()
                    comment.post = post
                    comment.owner = user
                    comment.text = serializer.validated_data['text']
                    comment.save()
                    return CustomResponse({
                        'message': ['Объект создан.']
                    }).good()
                return CustomResponse(
                    CustomErrors('post_id').object_not_found_error()
                ).bad()
            else:
                return CustomResponse(
                    CustomErrors('token').object_not_found_error()
                ).bad()
        else:
            return CustomResponse(serializer.errors).bad()


class GetPostAPIView(APIView):
    def get(self, request):
        serializer = GetPostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post.objects.get(pk=request.GET['pk'])
            serializer = GetPostSerializer(post)
            if serializer.is_valid():
                return CustomResponse(serializer.data).good()
            else:
                return CustomResponse(serializer.errors).bad()
        else:
            return CustomResponse(serializer.errors).bad()
