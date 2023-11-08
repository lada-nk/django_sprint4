from django.shortcuts import get_object_or_404, render

from blog.models import Post, Category


def index(request):
    """Возвращает главную страницу."""
    posts_number = 5
    post_list = Post.objects.custom_filter(
    ).select_related('category')[:posts_number]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    """Возвращает заданный пост."""
    post = get_object_or_404(
        Post.objects.custom_filter(),
        pk=pk
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Возвращает посты в заданной категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.posts.custom_filter()
    context = {'post_list': post_list,
               'category': category}
    return render(request, 'blog/category.html', context)
