from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.conf import settings
from .models import Post, Category, Comment
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.db.models import Count
from django.http import Http404

PAGINATE_BY = getattr(settings, 'PAGINATE_BY', 10)


def index(request):
    posts = Post.objects.select_related(
        'author', 'category', 'location'
    ).annotate(
        comment_count=Count('comments')
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    
    paginator = Paginator(posts, PAGINATE_BY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/index.html', {'page_obj': page_obj})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    # Проверка доступа: только автор может видеть неопубликованные
    if not post.is_published or not post.category.is_published or post.pub_date > timezone.now():
        if not (request.user.is_authenticated and request.user == post.author):
            raise Http404("Пост не найден")
    
    comments = post.comments.select_related('author')
    form = CommentForm()
    
    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    
    paginator = Paginator(posts, PAGINATE_BY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': page_obj
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    # Проверка: только автор может редактировать
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/create.html', {'form': form})

@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/edit_comment.html', {
        'form': form,
        'post_id': post_id
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('blog:post_detail', post_id=post.pk)

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    
    return render(request, 'blog/create.html', {
        'comment': comment,
        'post_id': post_id
    })

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('profile', username=request.user.username)
    
    return render(request, 'blog/create.html', {'form': None, 'post': post})