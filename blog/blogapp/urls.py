# blog/urls.py
from django.urls import path, include
from .views import post_list, post_detail, post_create, comment_create, rate_post, search_view

urlpatterns = [
    
    path('', post_list, name='post_list'),
    path('search/', view=search_view, name='search'),
    path('post/<int:pk>/', view=post_detail, name='post_detail'),
    path('post/create/', view=post_create, name='post_create'),
    path('post/<int:pk>/comment/', view=comment_create, name='comment_create'),
    path(route='post/<int:pk>/rate/', view= rate_post, name='rate_post'),
    
]
