from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from .models import Post
from .filters import PostFilter
from .forms import NewsForm, ArticleForm, DeleteForm


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-add_time'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


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
        return context


# Добавляем новое представление для создания новостей
class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "NW"
        return super().form_valid(form)


# Добавляем новое представление для создания статей
class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "AR"
        return super().form_valid(form)


# Добавляем новое представление для редактирования новостей
class NewsUpdate(UpdateView):
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


# Добавляем новое представление для редактирования статей
class ArticleUpdate(UpdateView):
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


# Добавляем новое представление для удаления новостей
class NewsDelete(DeleteView):
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


# Добавляем новое представление для удаления статей
class ArticleDelete(DeleteView):
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
