# from datetime import date
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CommentForm

# posts = [
# {
#     "slug": "hike-in-the-office",
#     "image": "coding.jpg",
#     "author": "Gaurav Mehtre",
#     "date": date(2025, 7, 15),
#     "title": "Office",
#     "excerpt": "Hiking is so much fun! There is nothing like hiking! Nusta hiking! Hiking Hiking Hiking Hiking Hiking",
#     "content": """
#             Lorem ipsum dolor, sit amet consectetur adipisicing elit.
#             Natus, voluptatem tempore voluptas, magni temporibus enim doloremque 
#             eius ratione excepturi vitae omnis sit 
#             sequi! Excepturi eius, architecto alias molestiae consectetur porro!

#             Lorem ipsum dolor, sit amet consectetur adipisicing elit.
#             Natus, voluptatem tempore voluptas, magni temporibus enim doloremque 
#             eius ratione excepturi vitae omnis sit 
#             sequi! Excepturi eius, architecto alias molestiae consectetur porro!

#             Lorem ipsum dolor, sit amet consectetur adipisicing elit.
#             Natus, voluptatem tempore voluptas, magni temporibus enim doloremque 
#             eius ratione excepturi vitae omnis sit 
#             sequi! Excepturi eius, architecto alias molestiae consectetur porro!
#     """
# }
# ]

# def get_date(post):
#     return post['date']


# Create your views here.
# def index(request):
#     sorted_posts = sorted(posts, key=get_date)
#     lastest_posts = sorted_posts[-3:]
#     return render(request, "blog/index.html", {
#         "posts": lastest_posts
#     })

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset =  super().get_queryset()
        data = queryset[:3]
        return data


# def index(request):
#     lastest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#          "posts": lastest_posts
#     })

class AllPostsView(ListView):
    template_name = "blog/all-post.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


# def all_posts(request):
#     all_post = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-post.html", {
#         "posts":all_post
#     })

class SinglePostView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post":post,
            "all_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
    
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post_details_page", args=[slug]))

        context = {
            "post":post,
            "all_tags":post.tags.all(),
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }

        return render(request, "blog/post-detail.html", context)             



# def single_post(request, slug):
#     # identified_post = next(post for post in posts if post['slug'] == slug )
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "all_tags" : identified_post.tags.all()
#     })

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")