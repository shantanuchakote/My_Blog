from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting_page"),
    path("posts/", views.AllPostsView.as_view(), name="posts_page"),
    path("posts/<slug>", views.SinglePostView.as_view(), name="post_details_page"),
    path("read_later", views.ReadLaterView.as_view(), name="read_later_page")
]
