from django.urls import path
from .views import PortfolioView, GalleryView, AboutView

urlpatterns = [
    path('', PortfolioView.as_view(), name='portfolio'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('about/', AboutView.as_view(), name='about'),
]