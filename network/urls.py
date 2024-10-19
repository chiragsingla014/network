
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost",views.newpost, name="newpost"),
    path("posts/<str:following>",views.posts, name="posts"),
    path("posts",views.posts, name="posts"),
    path("profile/<str:username>/",views.profile, name="profile"),
    path("edit/<str:post_id>",views.edit, name="edit"),
    path("likeunlike/<int:postid>",views.likeunlike, name="likeunlike"),
    path("followunfollow/<int:userid>",views.followunfollow, name="followunfollow")

]
