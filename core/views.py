from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .decorators import unauthenticated_user

from .forms import *
from .models import *


def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            print("success")
            return redirect('login')
        
    context = {
        'form': form
    }
        
    return render(request, 'core/register.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('error')

    return render(request, 'core/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def profilePage(request):
    normal_user = request.user.userinfo
    print(normal_user)

    form = ProfileForm(instance=normal_user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=normal_user)
        if form.is_valid():
            form.save()
            print('nice')
        else:
            print('haha')
    
    context = {
        'form': form,

        'normal_user': normal_user
    }

    return render(request, 'core/profile.html', context)



def send_request(request, id):
    from_user = request.user
    to_user = UserInfo.objects.get(id=id)
    friend_req = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    return redirect('home')

def accept_request(request, id):
    friend_req = FriendRequest.objects.get(id=id)
    user1 = request.user
    user2 = friend_req.from_user

    user1.friends.add(user2)
    user2.friends.add(user1)
    return redirect('home')



# @login_required(login_url='login')
# def homePage(request):
#     return render(request, 'core/home.html')


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'core/home.html', context)
    

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            print("nice")

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'core/home.html', context)
    

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'core/post_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'core/post_detail.html', context)
    

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'core/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={"pk": pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'core/post_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'core/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs={"pk": pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class ProfilePageView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserInfo.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        context = {
            'user': user,
            'profile': profile,
            'posts': posts
        }

        return render(request, 'core/profile.html', context)