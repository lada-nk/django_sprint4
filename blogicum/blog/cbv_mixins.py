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


class CommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}
        )


class CommentFormMixin:
    form_class = CommentForm


class AuthorCheck(UserPassesTestMixin):

    def test_func(self):
        return bool(self.request.user == self.get_object().author)


class UserCheck(UserPassesTestMixin):

    def test_func(self):
        return bool(self.request.user == self.get_object())


class PaginateByListView(ListView):
    paginate_by = POSTS_COUNT_ON_PAGE
