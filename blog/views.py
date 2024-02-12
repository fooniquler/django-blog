from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
        likes_count = self.get_object().likes.count()
        dislikes_count = self.get_object().dislikes.count()

        if self.request.user.is_authenticated:
            liked_by_user = self.get_object().likes.filter(id=self.request.user.id).exists()
            disliked_by_user = self.get_object().dislikes.filter(id=self.request.user.id).exists()
            if liked_by_user:
                context['liked_by_user'] = liked_by_user
            elif disliked_by_user:
                context['disliked_by_user'] = disliked_by_user

        context['likes_count'] = likes_count
        context['dislikes_count'] = dislikes_count
        context['popular_posts'] = popular_posts
        return context


@require_POST
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        is_liked = False
    else:
        post.likes.add(user)
        is_liked = True

        if user in post.dislikes.all():
            post.dislikes.remove(user)

    return JsonResponse({'likes': post.likes.count(), 'is_liked': is_liked, 'dislikes': post.dislikes.count()})


@require_POST
def dislike_post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    if user in post.dislikes.all():
        post.dislikes.remove(user)
        is_disliked = False
    else:
        post.dislikes.add(user)
        is_disliked = True

        if user in post.likes.all():
            post.likes.remove(user)

    return JsonResponse({'dislikes': post.dislikes.count(), 'is_disliked': is_disliked, 'likes': post.likes.count()})


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
