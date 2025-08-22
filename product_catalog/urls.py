from django.urls import path
from .views import HomePageView,ProductDetailView,CategoryProductListView,CartView,SearchResultsView,ProfileView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("product-detail/<int:pk>/",ProductDetailView.as_view(),name="product-detail"),
    path('category/<int:category_id>/',CategoryProductListView.as_view(), name='category-products'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/',CartView.as_view(), name='cart'),
]
