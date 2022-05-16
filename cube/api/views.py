from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


# Create your views here.
class SignView(TemplateView):
    template_name = 'sign/sign.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Auth | CuBe'
        return context


class AccountView(TemplateView):
    template_name = 'account/account-view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.filter(
            username=kwargs['username']
        )
        posts = Post.objects.filter(
            owner=user[0]
        )
        if user:
            context['user'] = user[0]
            context['posts'] = posts
        else:
            self.template_name = 'errors/404.html'
        context['page_title'] = f'{kwargs["username"]} | CuBe'
        return context


class AccountSubscribersView(TemplateView):
    template_name = 'account/show-users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.filter(
            username=kwargs['username']
        )
        if user:
            if user[0].show_subscribers or user[0] == self.request.user:
                context['user'] = user[0]
                context['users'] = user[0].subscribers.all()
                context['type'] = 'Подписчики'
                context['hidden_type'] = 'subscribers'
            else:
                self.template_name = 'errors/404.html'
        else:
            self.template_name = 'errors/404.html'
        context['page_title'] = f'{kwargs["username"]} | CuBe'
        return context


class AccountSubscriptionsView(TemplateView):
    template_name = 'account/show-users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.filter(
            username=kwargs['username']
        )
        if user:
            if user[0].show_subscriptions or user[0] == self.request.user:
                context['user'] = user[0]
                context['users'] = user[0].subscriptions.all()
                context['type'] = 'Подписки'
                context['hidden_type'] = 'subscriptions'
            else:
                self.template_name = 'errors/404.html'
        else:
            self.template_name = 'errors/404.html'
        context['page_title'] = f'{kwargs["username"]} | CuBe'
        return context


class AccountSettingsView(TemplateView):
    template_name = 'account/account-settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Настройки | CuBe'
        return context


class CreatePostView(TemplateView):
    template_name = 'post/post-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать | CuBe'
        return context


class ViewPostView(TemplateView):
    template_name = 'post/post-view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Запись | CuBe'
        post = Post.objects.filter(
            pk=kwargs['pk']
        )

        if post:
            context['post'] = post[0]

            comments = Comment.objects.filter(
                post_id=kwargs['pk']
            )
            context['comments'] = comments[::-1]
            context['comments_count'] = comments.count()
        else:
            self.template_name = 'errors/404.html'

        return context


class ApiDocsView(TemplateView):
    template_name = 'api_docs/api_docs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Api документация | CuBe'
        return context


class HomePageView(TemplateView):
    template_name = 'home_page/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Главная | CuBe'
        context['posts'] = Post.objects.all().order_by('likes')[::-1]
        return context

# errors
def custom_404_error(request, exception):
    return render(request, "errors/404.html", {})


def custom_500_error(request, exception=None):
    return render(request, "errors/500.html", {})
