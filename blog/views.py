from django.db import transaction
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from django.urls import reverse
from .tasks import moderate_post


class HomeView(ListView):
    model = Post
    template_name = 'home.html'

    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        return queryset


class PostView(DetailView):
    model = Post
    template_name = 'post_view.html'

    def get_object(self, queryset=None):
        with transaction.atomic():
            post = super().get_object(queryset)
            post.views_count += 1
            post.save()
            return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        popular_posts = Post.objects.order_by('-views_count')[:5]
        context['popular_posts'] = popular_posts
        return context


class MakePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'make_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        post_id = form.instance.id
        moderate_post.delay(post_id)
        return response


class EditPostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        post_id = form.instance.id
        post = Post.objects.get(id=post_id)
        post.status = 'moderated'
        post.save()
        moderate_post.delay(post_id)
        return response


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = '/'
