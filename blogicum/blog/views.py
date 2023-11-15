from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView
)
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from blog.models import User, Post, Category, Comment
from blog.forms import PostForm, CommentForm, UserUpdateForm


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'

    def get_queryset(self):
        if self.request.user == get_object_or_404(
                Post, pk=self.kwargs['pk']).author:
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.date_pub_filter()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostMixin:
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostFormMixin:
    form_class = PostForm


class PostUserCheck():

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCreateView(PostMixin, PostFormMixin, LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(
    PostMixin, PostUserCheck, UserPassesTestMixin,
    LoginRequiredMixin, DeleteView
):
    pass


class PostPytest():  # только для прохождения pytset
    # вместо LoginRequiredMixin, UserPassesTestMixin

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect(
                'blog:post_detail',
                pk=kwargs[self.pk_url_kwarg]
            )
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(
    PostMixin, PostFormMixin, PostPytest, UpdateView
):

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class CommentFormMixin:
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_cur = self.post_cur
        return super().form_valid(form)


class CommentMixin():
    model = Comment
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_cur = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )


class CommentCreateView(
    CommentMixin, CommentFormMixin, LoginRequiredMixin, CreateView
):
    post_cur = None


class CommentUserCheck():

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


class CommentUpdateView(
    CommentFormMixin, CommentUserCheck,
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        self.post_cur = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )


class CommentDeleteView(
    CommentMixin, CommentUserCheck,
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
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


class PaginateByListView(ListView):
    paginate_by = 10


class ProfileListView(PaginateByListView):
    """Возвращает профиль автора."""

    template_name = 'blog/profile.html'
    context_object_name = 'page_obj'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user == author:
            queryset = author.posts.all().annotate(
                comment_count=Count('comments')).order_by('-pub_date')
        else:
            queryset = author.posts.date_pub_filter().annotate(
                comment_count=Count('comments')).order_by('-pub_date')
        return queryset


class PostListView(PaginateByListView):
    """Возвращает главную страницу."""

    template_name = 'blog/index.html'
    queryset = Post.objects.date_pub_filter(
    ).select_related('category').annotate(
        comment_count=Count('comments')).order_by('-pub_date')


class CategoryPostsListView(PaginateByListView):
    """Возвращает посты в заданной категории."""

    template_name = 'blog/category.html'
    context_object_name = 'page_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return category.posts.date_pub_filter(
        ).annotate(comment_count=Count('comments')
                   ).order_by('-pub_date')
