from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment
from .forms import BlogForm, CommentForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.contrib import messages

# Reader Views
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blogApp/blog_list.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()
                return redirect('blog_detail', blog_id=blog.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blogApp/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'form': form
    })


# Writer Views
@login_required
def profile_view(request):
    return render(request, 'blogApp/profile.html')

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('my_blogs')
    else:
        form = BlogForm()
    return render(request, 'blogApp/create_blog.html', {'form': form})

@login_required
def my_blogs(request):
    blogs = Blog.objects.filter(user=request.user)
    return render(request, 'blogApp/my_blogs.html', {'blogs': blogs})

@login_required
def update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('my_blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogApp/create_blog.html', {'form': form})

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk, user=request.user)
    blog.delete()
    return redirect('my_blogs')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_list')
    else:
        form = UserCreationForm()
    return render(request, 'blogApp/signup.html', {'form': form})



@login_required
def my_blogs(request):
    blogs = Blog.objects.filter(user=request.user)
    return render(request, 'blogApp/my_blogs.html', {'blogs': blogs})


@login_required
def profile_view(request):
    return render(request, 'blogApp/profile.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('my_blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogApp/edit_blog.html', {'form': form})



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # or wherever you want
    else:
        form = SignUpForm()
    return render(request, 'blogApp/signup.html', {'form': form})


# @login_required
# def edit_blog(request, pk):
#     blog = get_object_or_404(Blog, pk=pk, author=request.user)

#     if request.method == 'POST':
#         form = BlogForm(request.POST, request.FILES, instance=blog)
#         if form.is_valid():
#             form.save()
#             return redirect('my_blogs')
#     else:
#         form = BlogForm(instance=blog)

#     return render(request, 'blogApp/edit_blog.html', {'form': form, 'blog': blog})


# @login_required
# def edit_blog(request, pk):
#     blog = get_object_or_404(Blog, pk=pk, author=request.user)

#     if request.method == 'POST':
#         form = BlogForm(request.POST, request.FILES, instance=blog)
#         if form.is_valid():
#             form.save()
#             return redirect('my_blogs')
#     else:
#         form = BlogForm(instance=blog)

#     return render(request, 'blogApp/edit_blog.html', {'form': form, 'blog': blog})


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, user=request.user)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully!")
            return redirect('my_blogs')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blogApp/edit_blog.html', {'form': form, 'blog': blog})

