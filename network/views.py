from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.core import serializers
from datetime import datetime
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


def default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




        

@login_required
def newpost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse(index))
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    form = PostForm()
    return render(request, "network/post.html", {
        "form": form
    })
        


@csrf_exempt
@login_required
def edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        print(request)

        data = json.loads(request.body)
        content = data.get('content')
        print(content)
        if content:
            post.content = content
            post.save()
            return JsonResponse({'success': True, 'content': post.content})
        else:
            return HttpResponseBadRequest("Invalid content")
    return HttpResponseBadRequest("Invalid request")


@login_required
def posts(request, following=""):
    if following == "":
        posts = Post.objects.all().order_by('-timestamp')
    elif following == "following":
        following_users = request.user.following.values_list('followee', flat=True)
        if not following_users:
            posts = Post.objects.none()  # Creates an empty queryset
        else:
            posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    else:
        user = User.objects.filter(username=following).first()
        posts = Post.objects.filter(user=user).order_by('-timestamp')
        print(posts)
    paginator = Paginator(posts, 10)
    page_obj =  paginator.get_page(request.GET.get('page'))
    serialized_posts = [post.serialize() for post in page_obj]
    for post in serialized_posts:
        print(post)
        if request.user.id == post["user"]["id"]:
            post["my"] = True
        else:
            post["my"] = False
    return JsonResponse({
        "posts": serialized_posts,
        "page": page_obj.number,
        "no_of_pages": paginator.num_pages,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
    })









@login_required
def profile(request, username):
    try:
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)

    except:
        return JsonResponse({
            "message":"no such user"
        })
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 10)
    page_obj =  paginator.get_page(request.GET.get('page'))
    serialized_posts = [post.serialize() for post in page_obj]


    return JsonResponse({
        "user": username,
        "isfollowing": User.is_following(self=request.user, user=user),
        "followers": profile.number_of_followers(),
        "followings": profile.number_of_followings(),
        "posts": serialized_posts,
        "page": page_obj.number,
        "no_of_pages": paginator.num_pages,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
    })
    








@csrf_exempt
@login_required
def likeunlike(request, postid):
    post = Post.objects.filter(id=postid).get()

    if request.method == 'GET':
        if Like.isliking(user=request.user, post=post):
            return JsonResponse({
                "liked": True
            })
        else:
            return JsonResponse({
                "liked": False
            })
    else:
        try:
            if Like.isliking(user=request.user, post=post):
                like = Like.objects.filter(liker=request.user, post=post).get()
                like.delete()
                post.likes = post.likes - 1
                post.save()
                return JsonResponse({
                    "liked": False,
                    "count": post.likes
                })
            else:

                like = Like(liker= request.user, post=post)
                like.save()
                post.likes = post.likes + 1
                post.save()
                return JsonResponse({
                    "liked": True,
                    "count": post.likes
                })
        except Exception as e:
            print(e)
            return JsonResponse({
                "error": "error"
            })



@csrf_exempt
@login_required
def followunfollow(request, userid):
    follower = request.user
    followee = User.objects.filter(id=userid).get()
    if request.method == 'POST':
        print('reached')
        if follower.is_following(followee):
            follow = Follow.objects.filter(follower=follower, followee=followee).get()
            follow.delete()
            count = Follow.objects.filter(followee=followee).count()
            return JsonResponse({
                "follow": False,
                "count": count
            })
        else:
            follow = Follow(follower=follower, followee=followee)
            follow.save()
            count = Follow.objects.filter(followee=followee).count()
            return JsonResponse({
                "follow": True,
                "count": count
            })
    else:

        if follower == followee :
            return JsonResponse({
                "follow": "self"
            })
        if follower.is_following(followee):
            return JsonResponse({
                "follow": True,
                "followeeid": followee.id
            })
        else:
            return JsonResponse({
                "follow": False,
                "followeeid": followee.id
            })


# def paginate_queryset(queryset, page_number, page_size=10):
#     paginator = Paginator(queryset, page_size)
#     page_obj = paginator.get_page(page_number)

#     paginated_data = {
#         'items': list(page_obj.object_list),
#         'page': page_obj.number,
#         'no_of_pages': paginator.num_pages,
#         'has_next': page_obj.has_next(),
#         'has_previous': page_obj.has_previous(),
#         'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
#         'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
#     }
#     return paginated_data