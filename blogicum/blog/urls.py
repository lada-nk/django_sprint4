from django.urls import include, path

from . import views

app_name = 'blog'

posts_pk = [
    path('', views.PostDetailView.as_view(), name='post_detail'),
    path('edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path(
        'comment/',
        views.CommentCreateView.as_view(), name='add_comment'
    ),
    path(
        'delete_comment/<int:comment_id>',
        views.CommentDeleteView.as_view(), name='delete_comment'
    ),
]

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path(
        'profile/<username>/',
        views.ProfileListView.as_view(), name='profile'
    ),
    path(
        'profile/<int:pk>/edit/',
        views.ProfileUpdateView.as_view(), name='edit_profile'
    ),
    path('posts/', include([
        path('<int:pk>/', include(posts_pk)),
        path(
            '<int:post_id>/edit_comment/<int:comment_id>',
            views.CommentUpdateView.as_view(), name='edit_comment'
        ),
        path('create/', views.PostCreateView.as_view(), name='create_post'),
    ])),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostsListView.as_view(), name='category_posts'
    ),
]
