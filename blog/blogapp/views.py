# Create your views here.
# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm, RatingForm, SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from typing import Any

@login_required
def post_list(request) -> HttpResponse:
    posts = Post.objects.all()
    return render(request=request, template_name='blog/post_list.html', context={'posts': posts})

@login_required
def post_detail(request, pk) -> HttpResponse:
    
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    ratings = post.ratings.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        rating_form = RatingForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.post = post
            rating.author = request.user
            rating.save()

    else:
        comment_form = CommentForm()
        rating_form = RatingForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'ratings': ratings, 'comment_form': comment_form, 'rating_form': rating_form})

@login_required
def post_create(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            print(request.user)  # Add this line to check the user
            return redirect('accounts:login')  # Redirect to your login URL
        form = PostForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_create.html', {'form': form})

@login_required
def rate_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.post = post
            rating.author = request.user
            rating.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = RatingForm()
    return render(request=request, template_name='blog/rate_post.html', context={'form': form})

def post_list(request) -> HttpResponse:
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)  # Show 5 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request=request, template_name='blog/post_list.html', context={'posts': posts})


def search_view(request):
    form = SearchForm()
    query = None
    results: list[Any] = []
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(content__icontains=query).order_by('-id')

    return render(request,'blog/search.html', {'form': form, 'query': query, 'results': results})
