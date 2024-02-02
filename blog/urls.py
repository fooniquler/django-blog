from django.urls import path, include
from .views import HomeView, PostView, MakePostView, EditPostView, DeletePostView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>', PostView.as_view(), name='post_view'),
    path('make_post/', MakePostView.as_view(), name='make_post'),
    path('edit_post/<int:pk>', EditPostView.as_view(), name="edit_post"),
    path('delete_post/<int:pk>', DeletePostView.as_view(), name='delete_post'),
]
