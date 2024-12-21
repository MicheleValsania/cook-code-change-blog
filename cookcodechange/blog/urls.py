from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Homepage
    path('tag/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<str:category>/', views.category_posts, name='category_posts'),

]
