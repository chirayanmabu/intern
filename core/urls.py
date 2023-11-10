from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.PostListView.as_view(), name="home"),

    path('restregister/', views.RegisterAPIView.as_view(), name="restregister"),
    path('restlogin/', views.LoginAPIView.as_view(), name="restlogin"),
    path('restuser/', views.UserViewAPI.as_view(), name="restuser"),
    path('restlogout/', views.LogoutViewAPI.as_view(), name="restlogout"),

    # function based
    # path('profile/', views.profilePage, name="profile"),

    # class based
    path('profile/<int:pk>', views.ProfilePageView.as_view(), name="profile"),
    path('profile-edit/<int:pk>', views.ProfileEditView.as_view(), name="profile-edit"),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
    path('post-edit/<int:pk>/', views.PostEditView.as_view(), name="post-edit"),
    path('post-delete/<int:pk>/', views.PostDeleteView.as_view(), name="post-delete"),

    path('post/<int:post_pk>/comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name="comment-delete"),

    # path('post/<int:pk>/like', views.Addlike.as_view(), name='like'),
    # path('like/<int:pk>', views.Addlike.as_view(), name='like'),
    path('like/', views.like, name='like'),

    path('search/', views.UserSearch.as_view(), name='search'),
    path('profile/<int:pk>/friends-list/', views.FriendsListView.as_view(), name='friends-list'),
    path('friend-requests/', views.FriendRequestView.as_view(), name='friend-requests'),

    path('profile/<int:pk>/add-friend', views.AddFriendView.as_view(), name="add-friend"),
    path('profile/<int:pk>/remove-friend', views.RemoveFriendView.as_view(), name="remove-friend"),
    # path('add-friend/<int:id>/', views.send_request, name="add-friend"),
    path('accept/<int:id>/', views.accept_request, name="accept"),

    path('chat/<str:room_name>', views.ChatRoom, name="chat-room"),


]