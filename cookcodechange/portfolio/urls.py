from django.urls import path
from .views import PortfolioView, GalleryView, AboutView

app_name = "portfolio"  # Application namespace

urlpatterns = [
    path("", PortfolioView.as_view(), name="portfolio"),
    path("gallery/", GalleryView.as_view(), name="gallery"),
    path("about/", AboutView.as_view(), name="about"),
]
