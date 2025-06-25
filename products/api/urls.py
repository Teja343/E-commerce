from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, CartViewSet, CartItemViewSet, OrderViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('cart', CartViewSet,basename='cart')
router.register('cart-items', CartItemViewSet,basename='cart-item')
router.register('orders', OrderViewSet,basename='order')

urlpatterns = router.urls   