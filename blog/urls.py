from django.urls import path
from . import views


urlpatterns = [
    path('',views.PostListView.as_view(),name='blog-home'),
    path('user/<str:username>/',views.UserPostListView.as_view(),name='user-posts'),
    path('post/detail/<int:pk>/',views.PostDetailView.as_view(),name='post-detail'),
    path('post/new/',views.PostCreateView.as_view(),name='post-create'),
    path('post/update/<int:pk>/',views.PostUpdateView.as_view(),name='post-update'),
    path('post/delete/<int:pk>/',views.PostDeleteView.as_view(),name='post-delete'),
    path('about/',views.about,name='blog-about'),
    path('add/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('like/post/', views.post_like, name='like'),
    path('share/post/<int:pk>/', views.share_post, name='share_post'),
    # path('add/commnt/ajax/', views.post_comment, name='add_comment_ajax'),
]
