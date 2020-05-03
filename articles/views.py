from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST        

from .models import Article, Comment
from .forms import ArticleForm, CommentForm

def index(request, tag=None):
    articles = Article.objects.prefetch_related('tags').order_by('-pk')
    keyword = count = 0
    if tag:
        articles = Article.objects.filter(tags__name__iexact=tag)
        keyword = tag
        count = Article.objects.filter(tags__name__iexact=tag).count()
    context = {
        'articles': articles,
        'keyword': keyword,
        'count': count,
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
            messages.add_message(request, messages.INFO, 'Your post has been successfully submitted!')
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/form.html', context)

@login_required
@require_POST
def delete(request):
    pk = request.POST.get('post_id')
    article = get_object_or_404(Article, id=pk)
    if request.user == article.user:
        article.delete()
        messages.add_message(request, messages.SUCCESS, 'Your post has been successfully deleted!')
    return redirect('articles:index')

@login_required                                                                                          
def update(request, pk):
    article = get_object_or_404(Article, id=pk)
    if request.user == article.user:
        if request.method == "POST":
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                article = form.save(commit=False)
                article.user = request.user
                article.save()
                messages.add_message(request, messages.SUCCESS, 'Your post has been successfully updated!')
                return redirect('articles:index')
        else:
            form = ArticleForm(instance=article)
        context = {
            'form': form,
            'article': article,
        }
        return render (request, 'articles/form.html', context)
    else:
        messages.warning(request, "Editting other people's post is not allowed")
        return redirect('articles:index')

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

def comments(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    form = CommentForm()
    context = {
        'article':article,
        'form':form,
    }
    return render(request, 'articles/comment.html', context)

@require_POST
def comment_create(request, article_id):
    if request.user.is_authenticated:
        article =  get_object_or_404(Article, id=article_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
        return redirect('articles:comments', article.pk)
    else:
        messages.warning(request, '댓글을 작성할 권한이 없습니다')
        return redirect('accounts:login')

@require_POST
def comment_delete(request, article_id, comment_id):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()
        return redirect('articles:comments', article_id)
    else:
        messages.danger(request, 'You do not have permission to delete this comment.')
        return redirect('accounts:login')

def search(request):
    keyword = request.POST.get('keyword')
    articles = Article.objects.filter(tags__name__iexact=keyword)
    count = Article.objects.filter(tags__name__iexact=keyword).count()
    context = {
        'articles': articles,
        'keyword': keyword,
        'count': count,
    }
    return render(request, 'articles/index.html', context)