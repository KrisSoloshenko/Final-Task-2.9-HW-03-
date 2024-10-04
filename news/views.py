from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.utils import timezone

import pytz

from .models import Post, Category, Subscriber
from .filters import PostFilter
from .forms import NewsForm, ArticleForm, DeleteForm


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-add_time'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context
    
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(self.request.META['HTTP_REFERER'])


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context
    
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(self.request.META['HTTP_REFERER'])


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    ordering = '-add_time'
    context_object_name = 'post_search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context
    
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(self.request.META['HTTP_REFERER'])


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "NW"
        post.author = self.request.user
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "AR"
        post.author = self.request.user
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        current_id = post.id
        if post.type == "NW":
            true_form = super().form_valid(form)
            return true_form
        return redirect(to=f'/news/articles/{current_id}/edit/')


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        current_id = post.id
        if post.type == "AR":
            true_form = super().form_valid(form)
            return true_form
        return redirect(to=f'/news/news/{current_id}/edit/')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    form_class = DeleteForm
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        current_id = self.object.id
        if self.object.type == "NW":
            true_form = super().form_valid(form)
            return true_form
        return redirect(to=f'/news/articles/{current_id}/delete/')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    form_class = DeleteForm
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        current_id = self.object.id
        if self.object.type == "AR":
            true_form = super().form_valid(form)
            return true_form
        return redirect(to=f'/news/news/{current_id}/delete/')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )