
from django.urls import path
from .views import IndexView,IndexView, AboutView, ContactView, get_json_view, ProductsView, CategoryProductsView, ProductsView, ProductDetailView

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('produits', ProductsView.as_view(), name='products'),
    path('produits/<slug:slug>/', CategoryProductsView.as_view(), name='prod-by-cat'),
    path('produits/<slug:slug>/', CategoryProductsView.as_view(), name='prod-by-sub-cat'),
    path('produits/produit/<slug:slug>/', ProductDetailView.as_view(), name='productDetail'),

]
