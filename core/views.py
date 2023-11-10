from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .decorators import unauthenticated_user
from django.dispatch import receiver

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed

from .forms import *
from .models import *
from .serializers import *

import jwt, datetime


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


def send_request(request, id):
    from_user = request.user
    to_user = UserProfile.objects.get(id=id)
    friend_req = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    return redirect('home')

def accept_request(request, id):
    friend_req = FriendRequest.objects.get(id=id)
    user1 = request.user
    user2 = friend_req.from_user

    user1.friends.add(user2)
    user2.friends.add(user1)
    return redirect('home')


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found.")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        
        response = Response()

        response.set_cookie(key="kwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }

        return response


class UserViewAPI(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")
        
        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)

        return Response(serializer.data)
    

class LogoutViewAPI(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        profile_list = UserProfile.objects.all()
        posts = Post.objects.filter(
            author__profile__friends__in=[logged_in_user.id]
            ).order_by('-created_on')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
            'profile_list': profile_list
        }

        return render(request, 'core/home.html', context)
    

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__friends__in=[logged_in_user.id]
            ).order_by('-created_on')
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            print("nice")
        else:
            print("haha")

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
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        # form = ProfileForm(instance=profile)

        friends = profile.friends.all()
        no_of_friends = len(friends)

        if (no_of_friends) == 0:
            is_friend = False

        for friend in friends:
            if friend == request.user:
                is_friend = True
                break
            else:
                is_friend = False

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            # 'form': form,
            'no_of_friends': no_of_friends,
            'is_friend': is_friend,
            
        }

        return render(request, 'core/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'bio', 'phone', 'profile_pic', 'banner_pic', 'address', 'dob', 'gender']

    template_name = 'core/profile-edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    

class AddFriendView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.friends.add(request.user)

        return redirect('profile', pk=profile.pk)

class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.friends.remove(request.user)

        return redirect('profile', pk=profile.pk)
    

class Addlike(LoginRequiredMixin, View):
     def post(self, request, pk, *args, **kwargs):
        post_obj = Post.objects.get(pk=pk)
        if request.POST.get('action') == "post":
            print("hello")
            result = ''
            id = int(request.POST.get('postid'))
            post = Post.objects.get(pk=pk)

            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                post.like_count -= 1
                post.save()
            else:
                post.likes.add(request.user)
                post.like_count += 1
                post.save()

        
            return JsonResponse({'result': result})
        

def like(request):
    if request.POST.get('action') == "post":
        print("hello")
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()
        print("result: ", result)
    

    
        return JsonResponse({'result': result})


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains = query)
        )

        context = {
            'profile_list': profile_list,
        }

        return render(request, 'core/search.html', context)


class FriendsListView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        friends = profile.friends.all()

        context = {
            'profile': profile,
            'friends': friends
        }

        return render(request, 'core/friends-list.html', context)


class FriendRequestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/friend-req.html')
    

def ChatRoom(request, room_name):

    
    context = {
        'room_name': room_name
    }

    return render(request, 'core/chatroom.html', context)

