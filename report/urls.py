from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView
from . import views

urlpatterns = [
    path('posts/list', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/add', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/upvote/', views.upvote_post, name='upvote_post'),
    path('post/<int:pk>/downvote/', views.downvote_post, name='downvote_post'),
    path('', views.home, name='home'), 
    path('home/', views.home, name='home'), 
    path('requests/', views.request_view, name='requests'),
    path('contacts/', views.contact_view, name='contact'),

]

app_name = "report"