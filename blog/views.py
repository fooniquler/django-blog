from django.db import transaction
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from django.urls import reverse


class HomeView(ListView):
    model = Post
    template_name = 'home.html'


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
        return super().form_valid(form)


class EditPostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'

    def get_success_url(self):
        post_id = self.kwargs['pk']
        return reverse('post_view', kwargs={'pk': post_id})


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = '/'
