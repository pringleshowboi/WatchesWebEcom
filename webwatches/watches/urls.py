from django.urls import path
from .views import WatchListCreateView, WatchDetailView
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'watches'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('watches/', views.product_list, name='product_list'),
    path('watches/<int:watch_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:watch_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('api/watches/', WatchListCreateView.as_view(), name='watch-list-create'),
    path('api/watches/<int:pk>/', WatchDetailView.as_view(), name='watch-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
