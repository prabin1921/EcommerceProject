from django.urls import path
from . import views
from .views import*
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)