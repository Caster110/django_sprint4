from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.conf import settings
from blog.models import Post, Comment
from django.db.models import Count

PAGINATE_BY = getattr(settings, 'PAGINATE_BY', 10)

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class RulesView(TemplateView):
    template_name = 'pages/rules.html'

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
    paginator = Paginator(posts, PAGINATE_BY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/profile.html', {
        'profile_user': user,
        'page_obj': page_obj,
        'is_owner': request.user.is_authenticated and request.user == user,
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})

def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)

def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)

def server_error(request):
    return render(request, 'pages/500.html', status=500)
