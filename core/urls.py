from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.PostListView.as_view(), name="home"),

    # function based
    # path('profile/', views.profilePage, name="profile"),

    # class based
    path('profile/<int:pk>', views.ProfilePageView.as_view(), name="profile"),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
    path('post-edit/<int:pk>/', views.PostEditView.as_view(), name="post-edit"),
    path('post-delete/<int:pk>/', views.PostDeleteView.as_view(), name="post-delete"),

    path('post/<int:post_pk>/comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name="comment-delete"),

    path('add-friend/<int:id>/', views.send_request, name="add-friend"),
    path('accept/<int:id>/', views.accept_request, name="accept"),
]