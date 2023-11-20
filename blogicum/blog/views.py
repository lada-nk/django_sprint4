from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (
    DetailView, CreateView, DeleteView, UpdateView
)
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import User, Post, Category, Comment
from blog.forms import CommentForm, UserUpdateForm
from blog.cbv_mixins import (
    PostMixin, PostFormMixin, CommentMixin, CommentFormMixin,
    PostUserCheck, CommentUserCheck, PaginateByListView
)


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'

    def get_queryset(self):
        # get_object_or_404 нужен для выбрасывания ошибки 404
        # при несуществующем посте
        if self.request.user != get_object_or_404(
                Post, pk=self.kwargs['pk']).author:
            return Post.objects.all().date_pub_filter()
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostCreateView(PostMixin, PostFormMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(
    PostMixin, PostUserCheck,
    LoginRequiredMixin, DeleteView
):
    pass


class PostUpdateView(
    PostMixin, PostFormMixin, PostUserCheck, UpdateView
):
    def handle_no_permission(self):
        post_detail_url = reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )
        return redirect(post_detail_url)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class CommentCreateView(
    CommentMixin, CommentFormMixin, CreateView
):
    model = Post
    post_cur = None

    def post(self, request, *args, **kwargs):
        self.post_cur = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_cur = self.post_cur
        return super().form_valid(form)


class CommentUpdateView(
    CommentFormMixin, CommentUserCheck, UpdateView
):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )


class CommentDeleteView(
    CommentMixin, CommentUserCheck, DeleteView
):
    pk_url_kwarg = 'comment_id'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user}
        )


class PostListView(PaginateByListView):
    """Возвращает главную страницу."""

    template_name = 'blog/index.html'
    queryset = Post.objects.date_pub_filter(
    ).select_related('category').comm_count()


class ProfileListView(SingleObjectMixin, PaginateByListView):
    """Возвращает профиль автора."""

    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context

    def get_queryset(self):
        if self.request.user.username != self.object.username:
            return self.object.posts.comm_count().date_pub_filter()
        return self.object.posts.comm_count().all()


class CategoryPostsListView(SingleObjectMixin, PaginateByListView):
    """Возвращает посты в заданной категории."""

    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=Category.objects.filter(is_published=True)
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context

    def get_queryset(self):
        return self.object.posts.date_pub_filter().comm_count()
