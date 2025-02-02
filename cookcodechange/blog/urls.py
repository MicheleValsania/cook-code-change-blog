from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),  # Landing page come root
    path('blog/', views.homepage, name='homepage'),  # Blog homepage
    path('codeur/', views.codeur_page, name='codeur'),  # Pagina codeur
    path('explorateur/', views.explorateur_page, name='explorateur'),  # Pagina explorateur
    path('tag/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),  # Tag posts
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Post detail
    path('category/<str:category>/', views.category_posts, name='category_posts'),  # Category posts
]
