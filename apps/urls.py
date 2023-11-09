from django.urls import path

from . import views


urlpatterns = [
    path("", views.PostsView.as_view()),
    path("filter/", views.FilterPostsView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", views.JsonFilterMovPostView.as_view(), name='json_filter'),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("author/<str:slug>/", views.AuthorView.as_view(), name="author_detail"),

    path('post/add/', views.PostCreate.as_view(), name='post_create'),
    path('<slug:slug>/edit/', views.PostUpdate.as_view(), name='post_edit'),
    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='post_delete'),

]
