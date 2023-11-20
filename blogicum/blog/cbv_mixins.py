from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

POSTS_COUNT_ON_PAGE = 10


class PostMixin(LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.object.author})


class PostFormMixin:
    form_class = PostForm


class PostUserCheck(UserPassesTestMixin):

    def test_func(self):
        post = self.get_object()
        return bool(self.request.user == post.author)


class CommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )


class CommentFormMixin:
    form_class = CommentForm


class CommentUserCheck(UserPassesTestMixin):

    def test_func(self):
        comment = self.get_object()
        return bool(self.request.user == comment.author)


class PaginateByListView(ListView):
    paginate_by = POSTS_COUNT_ON_PAGE
