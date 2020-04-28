from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm

def index(request, tag=None):
    articles = Article.objects.prefetch_related('tags').order_by('-pk')
    
    if tag:
        articles = Article.objects.filter(tags__name__iexact=tag)
    
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            article.tag_save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/form.html', context)


@login_required
def like(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    user = request.user
    # ver1)
    # if request.user in article.liked_users.all():
    
    # ver2)
    if article.liked_users.filter(id=user.id).exists():
        article.liked_users.remove(user) #id 넣어도 되지만 django는 똑똑해서 객체 자체를 넣어줘도 됨
    else:
        article.liked_users.add(user)
    return redirect('articles:index')


